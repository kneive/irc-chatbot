from .base import BaseParser, ParseResult
from typing import Optional, Dict
from .tags.tagFactory import TagFactory

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
        
            raw_tags['room-name'] = input[idx+1: input.find(' ', idx)].strip()

            # find start of message
            idx = input.find(' :', idx)
            if idx == -1:
                raise ValueError("(parse) PRIVMSG message is corrupted: no ' :' in message part")

            if 'vip/1' in input:
                raw_tags['vip'] = '1'
            else:
                raw_tags['vip'] = '0'

            if raw_tags.get('source-room-id')is not None:
                raw_tags['msg-id'] = 'sharedchatnotice'

            raw_tags['message-content'] = input[idx+2:]

            tags = TagFactory.createPrivmsgTag(raw_tags)

            return ParseResult(message_type='PRIVMSG', 
                               data=tags, 
                               raw_message=input)

        except Exception as e:
            print(input)
            print(f'(parse) PRIVMSG message is corrupted: {e.with_traceback} ({tags})')
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

    