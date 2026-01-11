import sys
sys.path.insert(0, '../src')
from client import IRCClient
import socket

def test_connection():
    """Test basic features of IRCClient"""
    print('='*50)
    print('Connection test')
    print('='*50)

    print('[TEST 1] Connecting to irc.libera.chat:6667')
    client = IRCClient('irc.libera.chat', 6667)

    if client.connect():
        print('Connection successful!')

        print('\n[TEST 2] Receiving server response')
        response = client.receive()

        if response:
            print(f'Received {len(response)} bytes')
            print('\nServer response (first 500 characters)')
            print(response[:500])
        
        else:
            print('No response received')

        print('\n[TEST 3] Send NICK command')
        client.send_raw('NICK foobar12345')
        print('Command sent')

        print('[TEST 4] Disconnect')
        client.disconnect()
        print('Disconnection successful')
    else:
        print('Connection failed')

def test_invalid_server():
    """Test connection to an invalid server"""
    
    print('='*50)
    print('Connection to an invalid server')
    print('='*50)

    print('[TEST 5] Connection to invalid.server:6667')
    client = IRCClient('invalid.server', 6667)

    if not client.connect():
        print('Correctly handled connection failure')
    else:
        print('Connection should have failed')

if __name__ == '__main__':
    test_connection()
    test_invalid_server()
    print('='*50)
    print('Tests complete')
    print('='*50)