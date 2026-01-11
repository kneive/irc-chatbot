import socket
import ssl
import threading
from auth import get_token
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
KEYS = PROJECT_ROOT / 'keyz'
LOGINDATA = KEYS / 'logins.key'
LOGFILE = PROJECT_ROOT / 'client.log'

class IRCClient:
    def __init__(self, nick, token, server='irc.chat.twitch.tv', port=6697, 
                 use_ssl=True, log_file=None):
        self.server = server
        self.port = port
        self.use_ssl = use_ssl
        self.nick = nick
        self.token = token if token.startswith('oauth:') else f'oauth:{token}'
        self.socket = None
        self.running = False
        self.log_file = log_file or LOGFILE
        self.log_handle = None


    def connect(self):
        """Connect to an IRC server."""
        try:
            # Open log file
            self.log_handle = open(self.log_file, 'a', encoding='utf-8')

            raw_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if self.use_ssl:
                ssl_context = ssl.create_default_context()
                self.socket = ssl_context.wrap_socket(raw_socket, server_hostname=self.server)

            else:
                self.socket = raw_socket
            
            self.socket.connect((self.server, self.port))
            print(f'connected to {self.server}:{self.port} (SSL={self.use_ssl})')
            return True
        
        except Exception as e:
            print(f'Connection failed: {e}')
            return False

    def send_raw(self, message):
        """Send a raw message to an IRC server."""
        if self.socket:
            self.socket.sendall(f'{message}\r\n'.encode('utf-8'))

    def login(self):
        """Send auth token and username to twitch server"""
        self.send_raw(f'PASS {self.token}')
        self.send_raw(f'NICK {self.nick}')
        #self.send_raw(f'USER {self.nick} 0 * :{self.nick}') ignored by twitch

    def request_capabilities(self, tags=True, commands=True, membership=True):
        """Request capabilities from Twitch IRC server"""
        caps = []
        if tags: caps.append('twitch.tv/tags')
        if commands: caps.append('twitch.tv/commands')
        if membership: caps.append('twitch.tv/membership')
        if caps:
            self.send_raw(f'CAP REQ :' + ' '.join(caps))
            print('Requested capabilities:', caps)

    def join_channel(self, channel):
        """Join an IRC channel."""
        if not channel.startswith('#'):
            channel = '#' + channel
        self.send_raw(f'JOIN {channel}')
        print(f'Joining {channel}')

    def send_message(self, channel, message):
        """Send a message to a channel."""
        if not channel.startswith('#'):
            channel = '#' + channel
        self.send_raw(f'PRIVMSG {channel} :{message}')

    def receive(self):
        """Receive data from a server."""
        buffer =''
        while self.running:
            try:
                data = self.socket.recv(4096)
                if not data:
                    print('Disconnected by server')
                    break
                buffer += data.decode('utf-8', errors='ignore')
                while '\r\n' in buffer:
                    line, buffer = buffer.split('\r\n', 1)
                    self.parse_line(line)

            except Exception as e:
                print(f'Receive error: {e}')
                break

    def receive_banner(self, timeout=2.0):
        """Read the server banner"""
        if not self.socket:
            return None
        prev_timeout = None
        try:
            prev_timeout = self.socket.gettimeout()
            self.socket.settimeout(timeout)
            data = self.socket.recv(4096)
            if not data:
                return None
            return data.decode('utf-8', errors='ignore')
        except socket.timeout:
            return None
        except Exception as e:
            print(f'receive error: {e}')
            return None
        finally:
            try:
                self.socket.settimeout(prev_timeout)
            except Exception:
                pass


    def parse_line(self, line):
        """Parse a single line received from the server"""
        # raw line
        print(line)

        if self.log_handle:
            self.log_handle.write(line + '\n')
            self.log_handle.flush()

        # keep alive
        if line.startswith('PING'):
            payload = line.split(' ', 1)[1] if ' ' in line else ':tmi.twitch.tv'
            self.send_raw(f'PONG {payload}')
            print(f'PONG')

    def input(self, default_channel=None):
        """Read user input and send to server"""
        while self.running:
            try:
                command = input()
            except EOFError:
                break

            if not command:
                continue
            # quit server
            if command.lower() == 'quit':
                self.running = False
                break
            # join channel
            elif command.lower().startswith('join '):
                channel = command[5:].strip()
                self.join_channel(channel)

            elif command.lower().startswith('say '):
                if not default_channel:
                    print('Set a default_channel or use: PRIVMSG #chan :message')
                    continue
                message = command[4:].strip()
                self.send_message(default_channel, message)
            else:
                # send raw message
                self.send_raw(command)
            


    def disconnect(self):
        """Close a connection"""
        self.running = False
        try:
            if self.socket:
                self.socket.close()
        finally:
            if self.log_handle:
                self.log_handle.close()
                self.log_handle = None
            print('Disconnected')

#example

if __name__ == '__main__':

    nick = 'nickname'
    token = get_token()

    if not nick or not token:
        print('Missing NICKNAME or AUTH TOKEN')
        exit(1)

    client = IRCClient(nick=nick, token=token, use_ssl=True)

    if client.connect():

        #login information
        client.login()
        client.request_capabilities(tags=True, commands=True, membership=True)
        client.join_channel('#channelname')
        
        #receive banner
        print(client.receive())

        #receive in different thread
        client.running = True
        receive_thread = threading.Thread(target=client.receive, daemon=True)
        receive_thread.start() 

        print("Type 'say <message>' to chat, 'join #channel' to join another channel, or 'quit' to leave the server.")

        try:
            client.input(default_channel=f'#{nick}')
        except KeyboardInterrupt:
            print('\nClosing connection...')
        finally:
            client.disconnect()