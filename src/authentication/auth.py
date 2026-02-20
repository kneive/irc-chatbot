import requests
import webbrowser
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
KEYS = PROJECT_ROOT / 'keyz'
TOKEN = KEYS / 'token'
REDIRECT_URI = 'http://localhost:3000'
HOST = 'localhost'
PORT = 3000

CREDENTIALS = KEYS / 'credentials.key'
SCOPES = ['chat:read', 'chat:edit']

class AuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.server.auth_code = parse_qs(urlparse(self.path).query).get('code', [None])[0]
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Authorization successful! You can close this window.')

def _request_token(client_id, client_secret, scopes):
    
    # Start server
    server = HTTPServer((HOST, PORT), AuthHandler)
    server.auth_code = None
    
    # Open browser
    auth_url = f"https://id.twitch.tv/oauth2/authorize?client_id={client_id}&redirect_uri={REDIRECT_URI}&response_type=code&scope={'+'.join(scopes)}"
    webbrowser.open(auth_url)
    
    print("Please authorize in your browser...")
    
    # Wait for authorization
    while server.auth_code is None:
        server.handle_request()
    
    # Request token
    token_data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': server.auth_code,
        'grant_type': 'authorization_code',
        'redirect_uri': REDIRECT_URI
    }
    
    response = requests.post("https://id.twitch.tv/oauth2/token", data=token_data)
    return response.json()

def _read_credentials():
    """Reads clinet_id and client_secret from credentials.key"""
    credentials = {}
    try:
        with open(CREDENTIALS, 'r') as f:
            for line in f:
                line = line.strip()
                if '=' in line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    credentials[key.strip()] = value.strip()
        if 'client_id' not in credentials or 'client_secret' not in credentials:
            raise ValueError('Missing client_id or client_secret in credentials.key')
        return credentials['client_id'], credentials['client_secret']
    except FileNotFoundError:
        print(f'Error: {CREDENTIALS} not found.')
        raise
    except Exception as e:
        print(f'Error reading credentials: {e}')
        raise

def _save_token(token_data, filename=TOKEN):
    """Save token data to file"""

    with open(filename, 'w') as fd:
        json.dump(token_data,  fd, indent=2)

    print(f'Token saved top {filename}.')

def _load_token(filename=TOKEN):
    """Load token data from file"""

    try:
        with open(filename, 'r') as fd:
            return json.load(fd)

    except FileNotFoundError:
        return None
    except Exception as e:
        print(f'Error loading token: {e}')
        return None

def get_token():
    """Get access token"""

    # Check whether token exists
    token_data = _load_token()

    if token_data and 'access_token' in token_data:
        return token_data['access_token']

    # Token does not exist
    client_id, client_secret = _read_credentials()
    token_data = _request_token(client_id, client_secret, SCOPES)

    # store token
    if 'access_token' in token_data:
        #_save_token(token_data)
        return token_data['access_token']
    else:
        return None