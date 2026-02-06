
import json
import time
import threading
import traceback
import socket
import ssl
from auth import get_token
from pathlib import Path
from parsers.parser import Saltshaker
from db.repositories import (AnnouncementRepository,
                             BitsRepository,
                             BitsbadgetierRepository, 
                             OnetapgiftRepository,
                             PaidupgradeRepository,
                             PayforwardRepository,
                             PrivmsgRepository,
                             RaidRepository, 
                             RoomRepository, 
                             RoomStateRepository, 
                             SubgiftRepository,
                             SubmysteryRepository, 
                             SubRepository, 
                             UserRoomRepository, 
                             UserlistRepository, 
                             UserRepository,
                             ViewerMilestoneRepository)

from db.services.service import SaltyService
from db.database import DatabaseManager

PROJECT_ROOT = Path(__file__).parent.parent
LOGINDATA = PROJECT_ROOT / 'keyz' / 'logins.key'
CONFIG = PROJECT_ROOT / 'config' / 'config.json'
LOGFILE = PROJECT_ROOT / 'logs' / 'log.log'

TOKEN = get_token()


class IRCClient:

    def __init__(self, nick, token, server='irc.chat.twitch.tv', port=6697, 
                 use_ssl=True, log_file=None, auto_reconnect=True, 
                 reconnect_delay=5, max_reconnect_attempts=None):
        self.server = server
        self.port = port
        self.use_ssl = use_ssl
        self.nick = nick
        self.token = token if token.startswith('oauth:') else f'oauth:{token}'
        self.socket = None
        self.running = False
        self.log_file = log_file or LOGFILE
        self.log_handle = None

        self.auto_reconnect = auto_reconnect
        self.reconnect_delay = reconnect_delay
        self.max_reconnect_attempts = max_reconnect_attempts
        self.reconnect_attempts = 0
        self.connected = False
        self.channels_joined = []
        self.last_ping_time = time.time()
        self.ping_timeout = 300

        db_manager = DatabaseManager('saltmine.db')
        announcement_repo = AnnouncementRepository(db_manager)
        bits_repo = BitsRepository(db_manager)
        bitsbadge_repo = BitsbadgetierRepository(db_manager)
        onetap_repo = OnetapgiftRepository(db_manager)
        paidupgrade_repo = PaidupgradeRepository(db_manager)
        payforward_repo = PayforwardRepository(db_manager)
        privmsg_repo = PrivmsgRepository(db_manager)
        raid_repo = RaidRepository(db_manager)
        room_repo = RoomRepository(db_manager)
        roomstate_repo = RoomStateRepository(db_manager)
        sub_repo = SubRepository(db_manager)
        subgift_repo = SubgiftRepository(db_manager)
        submystery_repo = SubmysteryRepository(db_manager)
        user_repo = UserRepository(db_manager)
        userRoom_repo = UserRoomRepository(db_manager)
        userlist_repo = UserlistRepository(db_manager)
        viewerMilestone_repo = ViewerMilestoneRepository(db_manager)

        self.service = SaltyService(announcement_repo=announcement_repo,
                                    bits_repo=bits_repo,
                                    bitsbadge_repo=bitsbadge_repo,
                                    onetap_repo=onetap_repo,
                                    paidupgrade_repo=paidupgrade_repo,
                                    payforward_repo=payforward_repo,
                                    privmsg_repo=privmsg_repo,
                                    raid_repo=raid_repo,
                                    room_repo=room_repo,
                                    roomstate_repo=roomstate_repo,
                                    sub_repo=sub_repo,
                                    subgift_repo=subgift_repo,
                                    submystery_repo=submystery_repo,
                                    user_repo=user_repo,
                                    userRoom_repo=userRoom_repo,
                                    userlist_repo=userlist_repo,
                                    viewerMilestone_repo=viewerMilestone_repo)
        
        self.parser = Saltshaker()

    def connect(self):
        """Connect to an IRC server."""
        try:

            # close existing socket
            if self.socket:
                try:
                    self.socket.close()
                except:
                    pass

            # Open log file
            if not self.log_handle:
                self.log_handle = open(self.log_file, 'a', encoding='utf-8')

            raw_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if self.use_ssl:
                ssl_context = ssl.create_default_context()
                self.socket = ssl_context.wrap_socket(raw_socket, server_hostname=self.server)

            else:
                self.socket = raw_socket
            
            self.socket.connect((self.server, self.port))
            self.connected = True
            self.reconnect_attempts = 0
            self.last_ping_time = time.time()

            print(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] Connected to {self.server}:{self.port} (SSL={self.use_ssl})')
            return True
        
        except Exception as e:
            self.connected = False
            print(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] Connection failed: {e}')
            return False

    def reconnect(self):
        """Attempt to reconnect to server"""
        print(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] Attempting to reconnect...')

        if self.connect():
            print(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] Connection successful.')

            self.login()
            self.request_capabilities(tags=True, commands=True, membership=True)

            time.sleep(1)

            if self.channels_joined:
                for channel in self.channels_joined:
                    self.join_channel(channel)
                    time.sleep(0.5)

            return True
        else:
            return False

    def send_raw(self, message):
        """Send a raw message to an IRC server."""

        try:
            if self.socket:
                self.socket.sendall(f'{message}\r\n'.encode('utf-8'))

        except Exception as e:
            print(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] Send error: {e}')
            self.connected = False

    def login(self):
        """Send auth token and username to twitch server"""

        self.send_raw(f'PASS {self.token}')
        self.send_raw(f'NICK {self.nick}')

    def request_capabilities(self, tags=True, commands=True, membership=True):
        """Request capabilities from Twitch IRC server"""

        caps = []
        if tags: caps.append('twitch.tv/tags')
        
        if commands: caps.append('twitch.tv/commands')
        
        if membership: caps.append('twitch.tv/membership')
        
        if caps:
            self.send_raw(f'CAP REQ :' + ' '.join(caps))
            print(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}]Requested capabilities: {caps}' )

    def join_channel(self, channel):
        """Join an IRC channel."""

        if not channel.startswith('#'):
            channel = '#' + channel

        if channel not in self.channels_joined:
            self.channels_joined.append(channel)

        self.send_raw(f'JOIN {channel}')
        print(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] Joining {channel}')

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

                # check connection
                if not self.connected:
                    print(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] Disconnected. Attempting to reconnect...')
                    if self.auto_reconnect:
                        self.reconnect_attempts += 1

                        if self.max_reconnect_attempts and self.reconnect_attempts > self.max_reconnect_attempts:
                            print(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] Max reconnect attempts reached. Full stop.')
                            break
                        
                        time.sleep(self.reconnect_delay)
                        if self.reconnect():
                            buffer = ''
                            continue
                        else:
                            continue
                    else:
                        break
                
                # check ping timeout
                if time.time() - self.last_ping_time > self.ping_timeout:
                    print(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] Ping timeout. Connection lost?')
                    self.connected = False
                    continue

                data = self.socket.recv(4096)
                if not data:
                    print(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}]Disconnected by server')
                    self.connected = False
                    continue
                
                buffer += data.decode('utf-8', errors='ignore')
                while '\r\n' in buffer:
                    line, buffer = buffer.split('\r\n', 1)
                    self.parse_line(line)
            
            except socket.timeout:
                continue

            except Exception as e:
                print(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] Receive error: {e}')
                self.connected = False
                time.sleep(1)

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
            print(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] Receive error: {e}')
            return None
        
        finally:
            try:
                self.socket.settimeout(prev_timeout)
            except Exception:
                pass


    def parse_line(self, line):
        """Parse a single line received from theroomstate server"""
        
        #output raw line
        #print(line)

        # log raw line
        #if self.log_handle:
        #    self.log_handle.write(line + '\n')
        #    self.log_handle.flush()

        # keep alive
        if line.startswith('PING'):
            self.last_ping_time = time.time()
            payload = line.split(' ', 1)[1] if ' ' in line else ':tmi.twitch.tv'
            self.send_raw(f'PONG {payload}')
            print(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] PONG')
            return
        
        try:
            parsed = self.parser.parse(line)
            if parsed:
                self.service.process_message(parsed)
        except Exception as e:
            print(line)
            print(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] Error processing line: {e}')
            print(f'Traceback: {traceback.format_exc()}')

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
                rest = command[4:].strip()

                if rest.startswith('#'):
                    parts = rest.split(' ', 1)
                    if len(parts) == 2:
                        channel = parts[0]
                        message = parts[1]
                        self.send_message(channel, message)
                    else:
                        print("Usage: 'say #channel message'")
                else:
                    if not default_channel:
                        print('Set a default_channel or use: PRIVMSG #chan :message')
                        continue
                    self.send_message(default_channel, rest)
            
            elif command.lower() == 'status':
                print(f"\n{'='*50}")
                print(f"Connection Status: {'Connected' if self.connected else 'Disconnected'}")
                print(f"Channels joined: {len(self.channels_joined)}")
                print(f"Channels: {', '.join(self.channels_joined)}")
                print(f"Last PING: {int(time.time() - self.last_ping_time)}s ago")
                print(f"Reconnect attempts: {self.reconnect_attempts}")
                print(f"{'='*50}\n")
            
            else:
                # send raw message
                self.send_raw(command)
            


    def disconnect(self):
        """Close a connection"""

        self.running = False
        self.connected = False

        try:
            if self.socket:
                self.socket.close()

        except:
            pass

        finally:
            if self.log_handle:
                try:
                    self.log_handle.close()
                
                except:
                    pass

                self.log_handle = None
            print(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] Disconnected')

def read_config():
        """Read configuration from config.json"""

        try:
            with open(CONFIG, 'r') as fd:
                config = json.load(fd)

            nickname = config.get('nickname')
            if not nickname:
                raise ValueError("Missing 'nickname' in config.json")
            
            channels = config.get('channels', [])

            return nickname, channels
        
        except FileNotFoundError:
            print (f'Error: {CONFIG} not found.')
            raise
        except json.JSONDecodeError as e:
            print(f'Error parsing config.json: {e}')
            raise
        except Exception as e:
            print(f'Error reading config: {e}')
            raise

if __name__ == '__main__':

    NICKNAME, CHANNELLIST = read_config()

    if not NICKNAME or not TOKEN:
        print('Missing NICKNAME or AUTH TOKEN')
        exit(1)

    client = IRCClient(nick=NICKNAME, 
                       token=TOKEN, 
                       use_ssl=True, 
                       auto_reconnect=True, 
                       reconnect_delay=5, 
                       max_reconnect_attempts=None)

    if client.connect():

        #login information
        client.login()
        client.request_capabilities(tags=True, commands=True, membership=True)        
        
        #receive banner
        print(client.receive_banner())

        if CHANNELLIST:
            for channel in CHANNELLIST:
                client.join_channel(channel)
                time.sleep(0.5)
        
        print(f"\n{'='*50}")
        print("Commands:")
        print("  say #channel message - Send message")
        print("  join #channel        - Join channel")
        print("  status               - Show connection status")
        print("  quit                 - Exit")
        print(f"{'='*50}\n")

        #receive in different thread
        client.running = True
        receive_thread = threading.Thread(target=client.receive, daemon=True)
        receive_thread.start() 

        try:
            client.input(default_channel=None)

        except KeyboardInterrupt:
            print('\nClosing connection...')
        finally:
            client.disconnect()

