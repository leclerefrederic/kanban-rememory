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
            401: 'Clé refusée. Recopie la clé API donnée par BotFather.',
            403: 'Accès refusé. Débloque le bot dans Telegram et envoie-lui /start.',
            409: 'Un webhook ou un autre lecteur utilise ce bot. Aucun réglage distant modifié.',
            429: 'Telegram limite les requêtes. Attends avant de réessayer.',
        }
        if method == 'sendMessage' and error.code >= 500:
            raise SetupError('Envoi incertain : vérifie Telegram avant de relancer un test.') from None
        raise SetupError(messages.get(error.code, f'Telegram a refusé la requête (HTTP {error.code}).')) from None
    except (OSError, URLError, ValueError):
        message = ('Envoi incertain : vérifie Telegram avant de relancer un test.'
                   if method == 'sendMessage' else 'Connexion impossible : vérifie le réseau puis relance.')
        raise SetupError(message) from None
    if not isinstance(result, dict) or result.get('ok') is not True or 'result' not in result:
        raise SetupError('Réponse Telegram non confirmée. Si un test était en cours, vérifie sa réception.')
    return result['result']


def validate(config):
    if (not isinstance(config, dict) or config.get('version') != 1
            or not isinstance(config.get('token'), str)
            or not re.fullmatch(r'[0-9]+:[A-Za-z0-9_-]+', config['token'])
            or not isinstance(config.get('chat_id'), str)
            or not re.fullmatch(r'[0-9]+', config['chat_id'])
            or not isinstance(config.get('events'), str)
            or not set(config['events'].split(',')).issubset(set(EVENTS.split(',')) | {''})):
        raise SetupError('Configuration invalide. Relance configure-telegram.py pour la remplacer.')
    return config


def load_config(path):
    try:
        if path.is_symlink():
            raise SetupError('La configuration ne doit pas être un lien symbolique.')
        if sys.platform != 'win32' and path.stat().st_mode & 0o077:
            raise SetupError('Configuration trop accessible. Rétablis les permissions privées (chmod 600).')
        return validate(json.loads(path.read_text(encoding='utf-8')))
    except FileNotFoundError:
        raise SetupError('Telegram non configuré. Lance configure-telegram.py sans argument.') from None
    except (OSError, ValueError):
        raise SetupError('Impossible de lire la configuration. Relance configure-telegram.py.') from None


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
        raise SetupError('Impossible de protéger le fichier Windows. Aucune clé enregistrée.') from None


def save_config(path, config):
    validate(config)
    if path.is_symlink():
        raise SetupError('Refus de remplacer un lien symbolique de configuration.')
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
    return ask(prompt + ' [o/N] ').strip().lower() in ('o', 'oui', 'y', 'yes')


def private_matches(updates, challenge):
    if not isinstance(updates, list):
        raise SetupError('Liste de messages Telegram invalide. Aucun réglage enregistré.')
    chats = {}
    for update in updates:
        message = update.get('message', {})
        chat = message.get('chat', {})
        if (message.get('text', '').strip() == challenge and chat.get('type') == 'private'
                and isinstance(chat.get('id'), int) and chat['id'] > 0):
            chats[str(chat['id'])] = chat
    return chats


def setup(path, ask=input, secret=getpass.getpass, call=api):
    print('Configuration Telegram — macOS / Windows. Ctrl+C annule sans remplacer la configuration.')
    if path.exists() and not yes('Une configuration existe. La remplacer après un nouveau test ?', ask):
        print('Annulé. Configuration conservée.')
        return 0
    # Do not fall back to echoed password input in redirected terminals.
    with warnings.catch_warnings():
        warnings.simplefilter('error', getpass.GetPassWarning)
        token = secret('Clé API du bot (saisie masquée) : ').strip()
    if not re.fullmatch(r'[0-9]+:[A-Za-z0-9_-]+', token):
        raise SetupError('Format de clé invalide. Utilise la clé API de BotFather, pas le nom du bot.')
    bot = call(token, 'getMe')
    if not isinstance(bot, dict) or not bot.get('is_bot') or not re.fullmatch(r'[A-Za-z0-9_]+', bot.get('username', '')):
        raise SetupError('Le bot ne peut pas être identifié. Rien enregistré.')
    print(f"Bot vérifié : {bot.get('first_name', '')} — @{bot['username']}")
    webhook = call(token, 'getWebhookInfo')
    if not isinstance(webhook, dict):
        raise SetupError('Réponse Telegram invalide. Aucun réglage enregistré.')
    if webhook.get('url'):
        raise SetupError('Ce bot utilise un webhook. Utilise un bot dédié aux notifications ; aucun webhook supprimé.')
    challenge = '/setup_' + secrets.token_hex(4)
    print(f"1. Ouvre https://t.me/{bot['username']} et appuie sur Démarrer si nécessaire.")
    print(f'2. Envoie exactement ce message au bot : {challenge}')
    print('Le bot ne répond pas automatiquement. Reviens ensuite dans ce Terminal.')
    while True:
        ask('3. Message envoyé ? Appuie sur Entrée pour rechercher ta conversation : ')
        updates = call(token, 'getUpdates', timeout=5, limit=100)
        chats = private_matches(updates, challenge)
        if len(chats) > 1:
            raise SetupError('Plusieurs conversations ont envoyé ce code. Relance pour obtenir un nouveau code.')
        if chats:
            chat_id, chat = next(iter(chats.items()))
            break
        print('Code non trouvé. Vérifie le lien du bot et le texte envoyé. Aucun identifiant à chercher.')
        if len(updates) >= 100:
            raise SetupError('Trop de messages en attente sur ce bot. Utilise un bot dédié ; aucun message supprimé.')
        if not yes('Réessayer après avoir envoyé le code dans cette conversation ?', ask):
            print('Annulé. Configuration précédente conservée.')
            return 0
    name = ' '.join(str(chat.get(key, '')) for key in ('first_name', 'last_name')).strip()
    print(f'Destinataire détecté : {name} (identifiant {chat_id}).')
    if not yes('Autoriser les notifications vers ce destinataire et envoyer un test ?', ask):
        print('Annulé. Aucun message envoyé, configuration précédente conservée.')
        return 0
    call(token, 'sendMessage', chat_id=chat_id, text='Remy : test de configuration Kanban Rememory.')
    print('Telegram a confirmé l’envoi du test.')
    if not yes('As-tu reçu le message dans cette conversation Telegram ?', ask):
        print('Réception non confirmée. Configuration précédente conservée ; ne recommence pas sans vérifier Telegram.')
        return 0
    save_config(path, {'version': 1, 'token': token, 'chat_id': chat_id,
                       'bot_username': bot['username'], 'events': EVENTS})
    print(f'Configuration enregistrée : {path}')
    print('Prêt. Les agents peuvent utiliser la commande run sans export ni clé dans leurs arguments.')
    return 0


def run_sender(path, script, arguments, send=False):
    config = load_config(path)
    if arguments[:1] == ['--']:
        arguments = arguments[1:]
    if not arguments:
        raise SetupError('Précise un événement après --, par exemple -- test.')
    if any(arg == '--send-to' or arg.startswith('--send-to=') for arg in arguments):
        raise SetupError('Utilise --send avant -- : le destinataire vient de la configuration confirmée.')
    script = script.resolve()
    if not script.is_file():
        raise SetupError('Script de notification introuvable. Vérifie --script.')
    environment = {**os.environ, 'TELEGRAM_BOT_TOKEN': config['token'],
                   'TELEGRAM_CHAT_ID': config['chat_id'], 'TELEGRAM_EVENTS': config['events']}
    if send:
        arguments = [*arguments, '--send-to', config['chat_id']]
    # No shell and no token on the command line. The selected candidate is not modified.
    return subprocess.run([sys.executable, str(script), *arguments], env=environment).returncode


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command')
    commands.add_parser('setup', help='configuration interactive (par défaut)')
    commands.add_parser('status', help='afficher la destination sans la clé')
    test = commands.add_parser('test', help='tester la configuration enregistrée')
    test.add_argument('--send', action='store_true', help='envoyer réellement le message de test')
    run = commands.add_parser('run', help='lancer le script existant avec la configuration enregistrée')
    run.add_argument('--script', type=Path, default=Path(__file__).with_name('notify-telegram.py'))
    run.add_argument('--send', action='store_true', help='envoyer au destinataire enregistré')
    run.add_argument('arguments', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    path = config_path()
    try:
        if args.command in (None, 'setup'):
            if not sys.stdin.isatty():
                raise SetupError('Lance ce fichier depuis un Terminal interactif : python3 configure-telegram.py (macOS) ou py -3 configure-telegram.py (Windows). Pas de script collé via python - ou de pipe.')
            return setup(path)
        if args.command == 'run':
            return run_sender(path, args.script, args.arguments, args.send)
        config = load_config(path)
        print(f"Configuration : @{config.get('bot_username', '?')} ; destinataire {config['chat_id']} ; fichier {path}")
        if args.command == 'test':
            if not args.send:
                print('Aucun envoi. Ajoute --send pour envoyer le test.')
                return 0
            api(config['token'], 'sendMessage', chat_id=config['chat_id'], text='Remy : test de configuration Kanban Rememory.')
            print('Telegram : envoi confirmé. Vérifie la réception dans Telegram.')
        return 0
    except (KeyboardInterrupt, EOFError):
        print('\nSaisie interrompue. Configuration précédente conservée.', file=sys.stderr)
        return 1
    except getpass.GetPassWarning:
        print('Saisie masquée indisponible. Ouvre un Terminal normal et relance.', file=sys.stderr)
        return 1
    except SetupError as error:
        print(str(error), file=sys.stderr)
        return 1
    except OSError:
        print('Opération locale impossible (fichier ou permissions). Configuration non confirmée ; vérifie avec status.', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
