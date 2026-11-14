"""Configure Telegram once, test it, and run a notification sender without shell exports."""

import argparse
import csv
import getpass
import io
import json
import os
from pathlib import Path
import re
import secrets
import subprocess
import sys
import tempfile
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
import warnings

EVENTS = 'attention,completed,delivered,blocked,closed'


class SetupError(Exception):
    pass


def config_path(platform=None, environ=None, home=None):
    platform = platform or sys.platform
    environ = os.environ if environ is None else environ
    home = Path.home() if home is None else Path(home)
    if platform == 'win32':
        base = Path(environ.get('LOCALAPPDATA') or home / 'AppData' / 'Local')
        return base / 'KanbanRememory' / 'telegram.json'
    return home / '.config' / 'kanban-rememory' / 'telegram.json'


def api(token, method, **parameters):
    request = Request(f'https://api.telegram.org/bot{token}/{method}',
                      data=json.dumps(parameters).encode(),
                      headers={'Content-Type': 'application/json'})
    try:
        with urlopen(request, timeout=20) as response:
            result = json.load(response)
    except HTTPError as error:
        messages = {
            401: 'Token rejected. Copy the API token from BotFather.',
            403: 'Access denied. Unblock the bot in Telegram and send it /start.',
            409: 'A webhook or another reader is using this bot. Remote settings were preserved.',
            429: 'Telegram is rate limiting requests. Wait before trying again.',
        }
        if method == 'sendMessage' and error.code >= 500:
            raise SetupError('Delivery uncertain. Check Telegram before sending another test.') from None
        raise SetupError(messages.get(error.code, f'Telegram rejected the request (HTTP {error.code}).')) from None
    except (OSError, URLError, ValueError):
        message = ('Delivery uncertain. Check Telegram before sending another test.'
                   if method == 'sendMessage' else 'Connection failed. Check your network and try again.')
        raise SetupError(message) from None
    if not isinstance(result, dict) or result.get('ok') is not True or 'result' not in result:
        raise SetupError('Telegram response could not be confirmed. If you sent a test, check whether it arrived.')
    return result['result']


def validate(config):
    if (not isinstance(config, dict) or config.get('version') != 1
            or not isinstance(config.get('token'), str)
            or not re.fullmatch(r'[0-9]+:[A-Za-z0-9_-]+', config['token'])
            or not isinstance(config.get('chat_id'), str)
            or not re.fullmatch(r'[0-9]+', config['chat_id'])
            or not isinstance(config.get('events'), str)
            or not set(config['events'].split(',')).issubset(set(EVENTS.split(',')) | {''})):
        raise SetupError('Invalid configuration. Run configure-telegram.py again to replace it.')
    return config


def load_config(path):
    try:
        if path.is_symlink():
            raise SetupError('The configuration file must not be a symbolic link.')
        if sys.platform != 'win32' and path.stat().st_mode & 0o077:
            raise SetupError('Configuration file permissions are too broad. Restore private permissions (chmod 600).')
        return validate(json.loads(path.read_text(encoding='utf-8')))
    except FileNotFoundError:
        raise SetupError('Telegram is not configured. Run configure-telegram.py without arguments.') from None
    except (OSError, ValueError):
        raise SetupError('Could not read the configuration. Run configure-telegram.py again.') from None


def protect_file(path, platform=None):
    """Called on an EMPTY newly created file, before writing any credential."""
    if (platform or sys.platform) != 'win32':
        path.chmod(0o600)
        return
    try:
        result = subprocess.run(['whoami', '/user', '/fo', 'csv', '/nh'],
                                check=True, capture_output=True, text=True)
        sid = next(csv.reader(io.StringIO(result.stdout)))[1]
        if not re.fullmatch(r'S-1-[0-9-]+', sid):
            raise ValueError('Invalid SID')
        subprocess.run(['icacls', str(path), '/inheritance:r', '/grant:r', f'*{sid}:F'],
                       check=True, capture_output=True, text=True)
    except (OSError, ValueError, IndexError, StopIteration, subprocess.CalledProcessError):
        raise SetupError('Could not secure the Windows file. No token was saved.') from None


def save_config(path, config):
    validate(config)
    if path.is_symlink():
        raise SetupError('Cannot replace a configuration file that is a symbolic link.')
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix='.telegram-', dir=path.parent)
    os.close(descriptor)
    temporary = Path(temporary)
    try:
        protect_file(temporary)
        with temporary.open('w', encoding='utf-8') as stream:
            json.dump(config, stream)
            stream.write('\n')
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def yes(prompt, ask):
    return ask(prompt + ' [y/N] ').strip().lower() in ('o', 'oui', 'y', 'yes')


def private_matches(updates, challenge):
    if not isinstance(updates, list):
        raise SetupError('Invalid Telegram update list. No settings were saved.')
    chats = {}
    for update in updates:
        message = update.get('message', {})
        chat = message.get('chat', {})
        if (message.get('text', '').strip() == challenge and chat.get('type') == 'private'
                and isinstance(chat.get('id'), int) and chat['id'] > 0):
            chats[str(chat['id'])] = chat
    return chats


def setup(path, ask=input, secret=getpass.getpass, call=api):
    print('Telegram setup for macOS and Windows. Press Ctrl+C to cancel and keep your existing configuration.')
    if path.exists() and not yes('Replace the existing configuration after a successful test?', ask):
        print('Canceled. Existing configuration kept.')
        return 0
    # Do not fall back to echoed password input in redirected terminals.
    with warnings.catch_warnings():
        warnings.simplefilter('error', getpass.GetPassWarning)
        token = secret('Bot API token (hidden input): ').strip()
    if not re.fullmatch(r'[0-9]+:[A-Za-z0-9_-]+', token):
        raise SetupError('Invalid token format. Enter the API token from BotFather.')
    bot = call(token, 'getMe')
    if not isinstance(bot, dict) or not bot.get('is_bot') or not re.fullmatch(r'[A-Za-z0-9_]+', bot.get('username', '')):
        raise SetupError('Could not identify the bot. No settings were saved.')
    print(f"Verified bot: {bot.get('first_name', '')} — @{bot['username']}")
    webhook = call(token, 'getWebhookInfo')
    if not isinstance(webhook, dict):
        raise SetupError('Invalid Telegram response. No settings were saved.')
    if webhook.get('url'):
        raise SetupError('This bot uses a webhook. Use a dedicated notification bot. The webhook was preserved.')
    challenge = '/setup_' + secrets.token_hex(4)
    print(f"1. Open https://t.me/{bot['username']} and press Start if needed.")
    print(f'2. Send this exact message to the bot: {challenge}')
    print('The bot does not reply automatically. Return to this terminal after sending the code.')
    while True:
        ask('3. Press Enter after sending the code to find your chat: ')
        updates = call(token, 'getUpdates', timeout=5, limit=100)
        chats = private_matches(updates, challenge)
        if len(chats) > 1:
            raise SetupError('Multiple chats sent this code. Run setup again to get a new code.')
        if chats:
            chat_id, chat = next(iter(chats.items()))
            break
        print('Code not found. Check the bot link and the text you sent. No chat ID lookup is needed.')
        if len(updates) >= 100:
            raise SetupError('This bot has too many pending messages. Use a dedicated bot. No messages were deleted.')
        if not yes('Try again after sending the code in this chat?', ask):
            print('Canceled. Previous configuration kept.')
            return 0
    name = ' '.join(str(chat.get(key, '')) for key in ('first_name', 'last_name')).strip()
    print(f'Recipient found: {name} (chat ID {chat_id}).')
    if not yes('Allow notifications to this recipient and send a test?', ask):
        print('Canceled. No message was sent. Previous configuration kept.')
        return 0
    call(token, 'sendMessage', chat_id=chat_id, text='Remy: Kanban Rememory setup test.')
    print('Telegram confirmed that the test was sent.')
    if not yes('Did you receive the message in this Telegram chat?', ask):
        print('Receipt was not confirmed. Previous configuration kept. Check Telegram before trying again.')
        return 0
    save_config(path, {'version': 1, 'token': token, 'chat_id': chat_id,
                       'bot_username': bot['username'], 'events': EVENTS})
    print(f'Configuration saved: {path}')
    print('Ready. Agents can use the run command with the saved configuration.')
    return 0


def run_sender(path, script, arguments, send=False):
    config = load_config(path)
    if arguments[:1] == ['--']:
        arguments = arguments[1:]
    if not arguments:
        raise SetupError('Specify an event after --, for example -- test.')
    if any(arg == '--send-to' or arg.startswith('--send-to=') for arg in arguments):
        raise SetupError('Use --send before --. The recipient comes from the confirmed configuration.')
    script = script.resolve()
    if not script.is_file():
        raise SetupError('Notification script not found. Check --script.')
    environment = {**os.environ, 'TELEGRAM_BOT_TOKEN': config['token'],
                   'TELEGRAM_CHAT_ID': config['chat_id'], 'TELEGRAM_EVENTS': config['events']}
    if send:
        arguments = [*arguments, '--send-to', config['chat_id']]
    # No shell and no token on the command line. The selected candidate is not modified.
    return subprocess.run([sys.executable, str(script), *arguments], env=environment).returncode


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command')
    commands.add_parser('setup', help='interactive setup (default)')
    commands.add_parser('status', help='show the recipient without revealing the token')
    test = commands.add_parser('test', help='test the saved configuration')
    test.add_argument('--send', action='store_true', help='send the test message')
    run = commands.add_parser('run', help='run the existing sender with the saved configuration')
    run.add_argument('--script', type=Path, default=Path(__file__).with_name('notify-telegram.py'))
    run.add_argument('--send', action='store_true', help='send to the saved recipient')
    run.add_argument('arguments', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    path = config_path()
    try:
        if args.command in (None, 'setup'):
            if not sys.stdin.isatty():
                raise SetupError('Run this file in an interactive terminal using python3 configure-telegram.py on macOS or py -3 configure-telegram.py on Windows. Piped input and python - are unsupported.')
            return setup(path)
        if args.command == 'run':
            return run_sender(path, args.script, args.arguments, args.send)
        config = load_config(path)
        print(f"Configuration: @{config.get('bot_username', '?')}, recipient {config['chat_id']}, file {path}")
        if args.command == 'test':
            if not args.send:
                print('Preview only. Add --send to send the test.')
                return 0
            api(config['token'], 'sendMessage', chat_id=config['chat_id'], text='Remy: Kanban Rememory setup test.')
            print('Telegram confirmed the send. Check your Telegram chat for the test.')
        return 0
    except (KeyboardInterrupt, EOFError):
        print('\nInput interrupted. Previous configuration kept.', file=sys.stderr)
        return 1
    except getpass.GetPassWarning:
        print('Hidden input unavailable. Open a regular terminal and try again.', file=sys.stderr)
        return 1
    except SetupError as error:
        print(str(error), file=sys.stderr)
        return 1
    except OSError:
        print('Local file or permission error. Use status to check the saved configuration.', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
