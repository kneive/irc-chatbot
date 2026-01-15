from .base import BaseParser, ParseResult
from typing import Optional, Dict

class MessageParser(BaseParser):

    def parseable(self, input:str) -> bool:
        """Check whether the input is parseable by this parser"""
        
        return ' PRIVMSG ' in input
    
    def parse(self, input:str) -> Optional[ParseResult]:
        """Parse input and return ParseResult or None"""

        try:
            separator = self._buildSeparator(input)
            
            # find end of tags
            boundary = input.find(separator)
            if boundary == -1:
                raise ValueError(f"(parse) PRIVMSG message is corrupted: cannot separate tags from message part. ({separator}, {boundary})")

            raw_tags = self._parseTags(input[1:boundary])

            # find room name
            idx = input.find('#', boundary+2)
            if idx == -1:
                raise ValueError("(parse) PRIVMSG message is corrupted: no '#' in message part")
        
            room = input[idx+1: input.find(' ', idx)]

            # find start of message
            idx = input.find(' :', idx)
            if idx == -1:
                raise ValueError("(parse) PRIVMSG message is corrupted: no ' :' in message part")

            message = input[idx+2:]
            
            tags = {}
            
            if 'source-room-id' in raw_tags:
                tags['room-id'] = raw_tags.get('source-room-id')
                tags['room-name'] = '#unknown'
            else:
                tags['room-id'] = raw_tags.get('room-id')
                tags['room-name'] = room

            tags['user-id'] = raw_tags.get('user-id')
            tags['display-name'] = raw_tags.get('display-name')
            tags['username'] = raw_tags.get('display-name').lower()
            tags['color'] = raw_tags.get('color')
            tags['badges'] = raw_tags.get('badges')
            tags['turbo'] = raw_tags.get('turbo')
            tags['returning-chatter'] = raw_tags.get('returning-chatter')
            tags['sub'] = raw_tags.get('subscriber','0')
            if ('vip/1' in raw_tags.get('source-badges') or 
                'vip/1' in raw_tags.get('badges')):
                tags['vip'] = '1'
            tags['mod'] = raw_tags.get('mod', '0')
            tags['user-type'] = raw_tags.get('user-type')

            tags['msg-id'] = raw_tags.get('id')
            tags['first-msg'] = raw_tags.get('first-msg')
            tags['reply-msg-id'] = raw_tags.get('reply-parent-msg-id', 'null')
            tags['reply-user-id'] = raw_tags.get('reply-parent-user-id', 'null')
            tags['reply-display-name'] = raw_tags.get('reply-parent-display-name', 'null')
            
            tags['thread-msg-id'] = raw_tags.get('reply-thread-parent-msg-id', 'null')
            tags['thread-user-id'] = raw_tags.get('reply-thread-parent-user-id', 'null')
            tags['thread-display-name'] = raw_tags.get('reply-thread-parent-display-name', 'null')
            
            # tags['tags'] = raw_tags
            tags['message-content'] = message

            return ParseResult(message_type='PRIVMSG', 
                               data=tags, 
                               raw_message=input)

        except Exception as e:
            print(f'(parse) PRIVMSG message is corrupted: {e} ({tags.items()})')
            result = ParseResult(message_type='PRIVMSG',
                                 data={},
                                 raw_message=input)
            result.is_valid = False
            result.error = str(e)
            return result

    def _buildSeparator(self, input:str) -> str:
        """Build separator for tags and message part"""

        try:
            start = input.find('display-name=')
            if start == -1:
                raise ValueError("PRIVMSG message is corrupted: no 'display-name'")
            
            start +=  len('display-name=')
            end = input.find(';', start)
            if end == -1:
                raise ValueError("(_buildSeparator) PRIVMSG message is corrupted: no ';' after display-name")
            
            return f' :{input[start:end]}'.lower()


        except Exception as e:
            print(f'Error parsing PRIVMSG: {e}')

    def _parseTags(self, input:str) -> Dict[str, str]:
        """Parse message tags from input string"""

        try:
            tags = {}
            for tag in input.split(';'):
                if '=' in tag:
                    key, value = tag.split('=', 1)
                    tags[key] = value if value else None
            
            return tags

        except ValueError as e:
            raise ValueError(f'(_parseTags) PRIVMSG message is corrupted {tags.items()}')

    