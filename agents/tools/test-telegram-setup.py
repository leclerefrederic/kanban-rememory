"""Run with Python 3.9+: isolated setup, persistence, CLI and sender integration tests."""

import contextlib
import functools
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import HTTPError, URLError

SCRIPT = Path(__file__).with_name('configure-telegram.py')
spec = importlib.util.spec_from_file_location('setup_telegram', SCRIPT)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
TOKEN = '123456789:PRIVATE_TEST_TOKEN'
CONFIG = {'version': 1, 'token': TOKEN, 'chat_id': '42', 'bot_username': 'RememoryNotifyBot', 'events': m.EVENTS}


def message(identifier=42, text='/setup_fixed', kind='private'):
    return {'message': {'text': text, 'chat': {'id': identifier, 'type': kind, 'first_name': 'Test'}}}


class SetupTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / 'config' / 'telegram.json'
        self.calls = []
        self.updates = [message()]

    def api(self, token, method, **values):
        self.assertEqual(token, TOKEN)
        self.calls.append((method, values))
        return {'getMe': {'is_bot': True, 'username': 'RememoryNotifyBot', 'first_name': 'Remy'},
                'getWebhookInfo': {'url': ''}, 'getUpdates': self.updates,
                'sendMessage': {'message_id': 1}}[method]

    def wizard(self, answers, api=None):
        responses = iter(answers)
        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch.object(m.secrets, 'token_hex', return_value='fixed'):
            code = m.setup(self.path, ask=lambda _: next(responses), secret=lambda _: TOKEN, call=api or self.api)
        self.assertNotIn(TOKEN, output.getvalue())
        return code, output.getvalue()

    def test_success_confirms_bot_recipient_delivery_and_saves(self):
        code, output = self.wizard(['', 'y', 'y'])
        self.assertEqual(code, 0)
        self.assertEqual(m.load_config(self.path), CONFIG)
        self.assertEqual([call[0] for call in self.calls], ['getMe', 'getWebhookInfo', 'getUpdates', 'sendMessage'])
        self.assertIn('does not reply automatically', output)
        if sys.platform != 'win32':
            self.assertEqual(self.path.stat().st_mode & 0o777, 0o600)

    def test_no_message_retry_without_manual_id(self):
        attempts = 0
        def api(token, method, **values):
            nonlocal attempts
            if method == 'getUpdates':
                attempts += 1
                return [] if attempts == 1 else [message()]
            return self.api(token, method, **values)
        _, output = self.wizard(['', 'y', '', 'y', 'y'], api)
        self.assertIn('No chat ID lookup is needed', output)
        self.assertTrue(self.path.exists())

    def test_ignores_old_start_wrong_code_and_groups(self):
        self.updates = [message(text='/start'), message(text='old'), message(kind='group'), message()]
        self.wizard(['', 'y', 'y'])
        self.assertEqual(m.load_config(self.path)['chat_id'], '42')

    def test_multiple_matches_refused_without_send(self):
        self.updates = [message(), message(43)]
        with self.assertRaisesRegex(m.SetupError, 'Multiple'):
            self.wizard([''])
        self.assertFalse(self.path.exists())
        self.assertNotIn('sendMessage', [c[0] for c in self.calls])

    def test_webhook_is_not_deleted(self):
        def api(token, method, **values):
            if method == 'getWebhookInfo':
                return {'url': 'https://example.invalid/hook'}
            return self.api(token, method, **values)
        with self.assertRaisesRegex(m.SetupError, 'webhook'):
            self.wizard([], api)
        self.assertFalse(self.path.exists())
        self.assertEqual([c[0] for c in self.calls], ['getMe'])

    def test_cancel_existing_config_and_recipient_refusal(self):
        m.save_config(self.path, CONFIG)
        original = self.path.read_bytes()
        self.wizard(['n'])
        self.assertEqual(self.calls, [])
        self.wizard(['y', '', 'n'])
        self.assertEqual(self.path.read_bytes(), original)
        self.assertNotIn('sendMessage', [c[0] for c in self.calls])

    def test_receive_not_confirmed_preserves_old_config(self):
        m.save_config(self.path, {**CONFIG, 'chat_id': '99'})
        original = self.path.read_bytes()
        self.wizard(['y', '', 'y', 'n'])
        self.assertEqual(self.path.read_bytes(), original)

    def test_failed_test_does_not_replace_config_or_retry(self):
        m.save_config(self.path, CONFIG)
        original = self.path.read_bytes()
        def api(token, method, **values):
            if method == 'sendMessage':
                self.calls.append((method, values))
                raise m.SetupError('Envoi uncertain')
            return self.api(token, method, **values)
        with self.assertRaisesRegex(m.SetupError, 'uncertain'):
            self.wizard(['y', '', 'y'], api)
        self.assertEqual(self.path.read_bytes(), original)
        self.assertEqual(sum(c[0] == 'sendMessage' for c in self.calls), 1)

    def test_permission_failure_leaves_old_config_and_no_secret_temp(self):
        m.save_config(self.path, CONFIG)
        original = self.path.read_bytes()
        with patch.object(m, 'protect_file', side_effect=m.SetupError('ACL refused')):
            with self.assertRaises(m.SetupError):
                m.save_config(self.path, {**CONFIG, 'chat_id': '99'})
        self.assertEqual(self.path.read_bytes(), original)
        self.assertEqual(list(self.path.parent.glob('.telegram-*')), [])

    def test_atomic_replace_failure_preserves_previous_config(self):
        m.save_config(self.path, CONFIG)
        original = self.path.read_bytes()
        with patch.object(m.os, 'replace', side_effect=OSError('disk failure')):
            with self.assertRaises(OSError):
                m.save_config(self.path, {**CONFIG, 'chat_id': '99'})
        self.assertEqual(self.path.read_bytes(), original)
        self.assertEqual(list(self.path.parent.glob('.telegram-*')), [])

    def test_malformed_saved_values_are_refused(self):
        for change in ({'chat_id': 42}, {'token': None}, {'events': ['attention']}, {'events': 'unknown'}):
            with self.subTest(change=change), self.assertRaises(m.SetupError):
                m.validate({**CONFIG, **change})

    def test_paths_on_macos_and_windows(self):
        home = Path(self.directory.name)
        self.assertEqual(m.config_path('darwin', {}, home), home / '.config/kanban-rememory/telegram.json')
        self.assertEqual(m.config_path('win32', {'LOCALAPPDATA': str(home / 'Local')}, home),
                         home / 'Local/KanbanRememory/telegram.json')
        self.assertEqual(m.config_path('win32', {}, home), home / 'AppData/Local/KanbanRememory/telegram.json')

    def test_windows_acl_applied_to_empty_file_before_secret_write(self):
        real_protect = m.protect_file
        calls = []
        def run(args, **kwargs):
            calls.append(args)
            if args[0] == 'icacls':
                self.assertEqual(Path(args[1]).read_bytes(), b'')
            return subprocess.CompletedProcess(args, 0, stdout='"machine\\user","S-1-5-21-123-1001"\n')
        with patch.object(m.subprocess, 'run', side_effect=run), patch.object(
                m, 'protect_file', side_effect=lambda p: real_protect(p, 'win32')):
            m.save_config(self.path, CONFIG)
        self.assertEqual(calls[0], ['whoami', '/user', '/fo', 'csv', '/nh'])
        self.assertEqual(calls[1][2:], ['/inheritance:r', '/grant:r', '*S-1-5-21-123-1001:F'])
        self.assertEqual(json.loads(self.path.read_text()), CONFIG)

    def test_windows_acl_failure_refuses_save(self):
        empty = Path(self.directory.name) / 'empty'
        empty.touch()
        with patch.object(m.subprocess, 'run', side_effect=subprocess.CalledProcessError(1, 'whoami')):
            with self.assertRaisesRegex(m.SetupError, 'No token'):
                m.protect_file(empty, 'win32')
        self.assertEqual(empty.read_bytes(), b'')

    def test_api_errors_are_actionable_and_redact_token(self):
        for code, expected in [(401, 'Token rejected'), (403, 'Unblock'), (409, 'another reader'), (429, 'rate limiting'), (500, 'uncertain')]:
            with self.subTest(code=code), patch.object(m, 'urlopen', side_effect=HTTPError(
                    f'https://api.telegram.org/bot{TOKEN}/sendMessage', code, TOKEN, {}, None)):
                with self.assertRaises(m.SetupError) as error:
                    m.api(TOKEN, 'sendMessage', chat_id='42')
                self.assertIn(expected, str(error.exception))
                self.assertNotIn(TOKEN, str(error.exception))
        with patch.object(m, 'urlopen', side_effect=URLError(TOKEN)):
            with self.assertRaisesRegex(m.SetupError, 'uncertain'):
                m.api(TOKEN, 'sendMessage')

    def test_api_posts_parameters_and_checks_response_without_exposing_key(self):
        with patch.object(m, 'urlopen', return_value=io.BytesIO(b'{"ok":true,"result":{"id":42}}')) as opened:
            self.assertEqual(m.api(TOKEN, 'getUpdates', timeout=5, limit=100), {'id': 42})
        request = opened.call_args.args[0]
        self.assertEqual(request.get_method(), 'POST')
        self.assertEqual(json.loads(request.data), {'timeout': 5, 'limit': 100})
        self.assertEqual(opened.call_args.kwargs['timeout'], 20)
        for reply in (b'not JSON', b'{"ok":false}', b'[]'):
            with patch.object(m, 'urlopen', return_value=io.BytesIO(reply)):
                with self.assertRaises(m.SetupError) as error:
                    m.api(TOKEN, 'sendMessage', chat_id='42', text='test')
                self.assertNotIn(TOKEN, str(error.exception))

    def test_status_and_test_preview_do_not_send_or_reveal_token(self):
        m.save_config(self.path, CONFIG)
        for command in ('status', 'test'):
            with patch.object(m, 'config_path', return_value=self.path), patch.object(
                    sys, 'argv', [str(SCRIPT), command]), patch.object(m, 'api') as api:
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    self.assertEqual(m.main(), 0)
                api.assert_not_called()
                self.assertIn('42', output.getvalue())
                self.assertNotIn(TOKEN, output.getvalue())

    def test_no_token_disclosure_on_invalid_config(self):
        self.path.parent.mkdir()
        self.path.write_text(TOKEN)
        self.path.chmod(0o600)
        with self.assertRaises(m.SetupError) as error:
            m.load_config(self.path)
        self.assertNotIn(TOKEN, str(error.exception))

    @unittest.skipIf(sys.platform == 'win32', 'POSIX mode protection')
    def test_public_config_and_symlink_refused(self):
        m.save_config(self.path, CONFIG)
        self.path.chmod(0o644)
        with self.assertRaisesRegex(m.SetupError, 'too broad'):
            m.load_config(self.path)
        link = self.path.with_name('link.json')
        link.symlink_to(self.path)
        with self.assertRaisesRegex(m.SetupError, 'symbolic'):
            m.save_config(link, CONFIG)

    def test_new_process_inherits_saved_config_without_exports(self):
        m.save_config(self.path, CONFIG)
        sender = Path(self.directory.name) / 'candidate sender.py'
        result_file = sender.with_suffix('.json')
        sender.write_text('import os, sys, json\nfrom pathlib import Path\n'
                          'Path(__file__).with_suffix(".json").write_text(json.dumps({'
                          '"args": sys.argv[1:], "token_matches": os.environ["TELEGRAM_BOT_TOKEN"] == '
                          + repr(TOKEN) + ', "chat": os.environ["TELEGRAM_CHAT_ID"], '
                          '"events": os.environ["TELEGRAM_EVENTS"]}))\n')
        original = sender.read_bytes()
        with patch.dict(os.environ, {'TELEGRAM_BOT_TOKEN': 'wrong-token'}):
            self.assertEqual(m.run_sender(self.path, sender, ['--', 'attention', '--text', 'à valider'], True), 0)
        result = json.loads(result_file.read_text())
        self.assertTrue(result['token_matches'])
        self.assertEqual(result['args'], ['attention', '--text', 'à valider', '--send-to', '42'])
        self.assertNotIn(TOKEN, result['args'])
        self.assertEqual(sender.read_bytes(), original)
        m.run_sender(self.path, sender, ['test'])
        self.assertEqual(json.loads(result_file.read_text())['args'], ['test'])
        with self.assertRaisesRegex(m.SetupError, 'recipient'):
            m.run_sender(self.path, sender, ['test', '--send-to=99'])

    def test_here_document_or_pipe_fails_with_instructions_not_eof(self):
        # Inspect ASCII markers as bytes: Windows child output uses its own code page.
        result = subprocess.run([sys.executable, str(SCRIPT)], input=b'', capture_output=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn(b'interactive terminal', result.stderr)
        self.assertNotIn(b'Traceback', result.stderr)

    def test_module_alerts_use_shared_receipts_without_colliding(self):
        spec = importlib.util.spec_from_file_location('notify_telegram', SCRIPT.with_name('notify-telegram.py'))
        notifier = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(notifier)
        root = Path(self.directory.name)
        git_dir = root / 'git-common'
        git_dir.mkdir()
        manifest = {
            'schema_version': 1,
            'project': {'id': 'example', 'name': 'Example solution'},
            'shared': {'memory': 'project/rememory', 'sources': ['src']},
            'modules': {
                'a': {'workspace': 'project/modules/a'},
                'b': {'workspace': 'project/modules/b'},
            },
            'execution': {
                'active_deliveries_per_module': 1, 'branch_required': True,
                'worktree_required': True, 'concurrent_integrations': 1,
            },
        }
        (root / 'project.json').write_text(json.dumps(manifest))
        sent = []

        def fake_sender(token, chat, text):
            self.assertEqual((token, chat), (TOKEN, '42'))
            sent.append(text)

        args = ['notify-telegram.py', 'completed', '--task', 'Export', '--id', 'export',
                '--reference', 'CARD-00000001', '--text', 'Export vérifié.',
                '--next-action', 'Aucune action requise.', '--language', 'fr',
                '--chat-name', 'Codex · Export', '--send-to', '42']
        with patch.object(notifier, '__file__', str(root / 'agents/tools/notify-telegram.py')), \
                patch.object(notifier.subprocess, 'check_output', return_value=str(git_dir)), \
                patch.object(notifier, 'notify', functools.partial(notifier.notify, sender=fake_sender)), \
                patch.dict(os.environ, {'TELEGRAM_CHAT_ID': '42', 'TELEGRAM_BOT_TOKEN': TOKEN,
                                        'TELEGRAM_EVENTS': 'completed'}), \
                contextlib.redirect_stdout(io.StringIO()):
            errors = io.StringIO()
            with patch.object(sys, 'argv', args), contextlib.redirect_stderr(errors), self.assertRaises(SystemExit) as exit:
                notifier.main()
            self.assertEqual(exit.exception.code, 2)
            self.assertIn('Choose a module explicitly', errors.getvalue())
            self.assertFalse(sent)
            for module_args in (['--module', 'a'], ['--module', 'b'],
                                ['--module', 'a', '--project', 'Renamed solution']):
                with patch.object(sys, 'argv', [*args, *module_args]):
                    self.assertEqual(notifier.main(), 0)
        self.assertEqual(len(sent), 2)
        for module, message in zip(('a', 'b'), sent):
            self.assertIn('Projet: Example solution', message)
            self.assertIn(f'Référence: {module} / CARD-00000001', message)
            self.assertIn('Prochaine action: Aucune action requise.', message)

    @unittest.skipIf(sys.platform == 'win32', 'Real POSIX terminal; Windows needs live acceptance')
    def test_real_terminal_accepts_all_answers_without_echoing_token(self):
        import pty
        import select
        import time
        harness = Path(self.directory.name) / 'interactive.py'
        harness.write_text('import importlib.util\nfrom pathlib import Path\n'
            f's=importlib.util.spec_from_file_location("m", {str(SCRIPT)!r})\n'
            'm=importlib.util.module_from_spec(s);s.loader.exec_module(m)\n'
            f'm.config_path=lambda:Path({str(self.path)!r})\n'
            'm.secrets.token_hex=lambda n:"fixed"\n'
            'def call(token, method, **kwargs):\n'
            f' return {{"getMe":{{"is_bot":True,"username":"RememoryNotifyBot"}},"getWebhookInfo":{{"url":""}},"getUpdates":[{message()!r}],"sendMessage":{{"message_id":1}}}}[method]\n'
            'wizard=m.setup\nm.setup=lambda path:wizard(path, call=call)\nraise SystemExit(m.main())\n')
        pid, fd = pty.fork()
        if pid == 0:
            os.execl(sys.executable, sys.executable, str(harness))
        data = b''
        def until(marker):
            nonlocal data
            deadline = time.monotonic() + 10
            while marker.encode() not in data:
                if time.monotonic() >= deadline:
                    self.fail('Terminal did not reach expected prompt: ' + marker)
                if select.select([fd], [], [], 0.2)[0]:
                    data += os.read(fd, 4096)
        try:
            until('hidden input')
            os.write(fd, (TOKEN + '\n').encode())
            until('Press Enter after sending the code')
            os.write(fd, b'\n')
            until('Allow notifications')
            os.write(fd, b'y\n')
            until('Did you receive')
            os.write(fd, b'y\n')
            until('Configuration saved')
            _, status = os.waitpid(pid, 0)
            self.assertEqual(os.waitstatus_to_exitcode(status), 0)
            self.assertNotIn(TOKEN.encode(), data)
            self.assertEqual(m.load_config(self.path)['chat_id'], '42')
        finally:
            os.close(fd)


if __name__ == '__main__':
    unittest.main()
