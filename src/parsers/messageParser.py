from .base import BaseParser, ParseResult
from typing import Optional, Dict
from .tags.tagFactory import TagFactory
import traceback

class MessageParser(BaseParser):

    def parseable(self, input:str) -> bool:
        """Check whether the input is parseable by this parser"""
        
        return ' PRIVMSG ' in input
    
    def parse(self, input:str) -> Optional[ParseResult]:
        """Parse input and return ParseResult or None"""

        tags = {}

        try:
            # find end of tags part
            temp_idx = input.find('user-type=')
            if temp_idx == -1:
                raise ValueError(f"(parse) PRIVMSG message is corrupted: no 'user-type'.")

            boundary = input.find(' :', temp_idx)
            if boundary == -1:
                raise ValueError(f"(parse) PRIVMSG message is corrupted: cannot separate tags from message part. No ' :' after 'user-type'")

            raw_tags = self._parseTags(input[1:boundary])

            # check for vip badge
            if 'vip/1' in input:
                raw_tags['vip'] = '1'
            else:
                raw_tags['vip'] = '0'

            # check for sharedchat
            if raw_tags.get('source-room-id') is not None:
                raw_tags['msg-id'] = 'sharedchatnotice'

            # find room name
            idx = input.find('#', boundary+2)
            if idx == -1:
                raise ValueError("(parse) PRIVMSG message is corrupted: no '#' in message part")
        
            raw_tags['room-name'] = input[idx+1: input.find(' ', idx)].strip()
            raw_tags['source-room-name'] = '#unknown'

            # find start of message part
            idx = input.find(' :', idx)
            if idx == -1:
                raise ValueError("(parse) PRIVMSG message is corrupted: no ' :' in message part")

            raw_tags['message-content'] = input[idx+2:]

            # replace \\s
            if raw_tags.get('reply-parent-msg-body') is not None:
                raw_tags['reply-parent-msg-body'] = raw_tags.get('reply-parent-msg-body').replace('\s', ' ')

            tags = TagFactory.createPrivmsgTag(raw_tags)

            return ParseResult(message_type='PRIVMSG', 
                               data=tags, 
                               raw_message=input)

        except Exception as e:
            print(input)
            print(f'(parse) PRIVMSG message is corrupted: {e} ({tags})')
            print(f'Traceback: {traceback.format_exc()}')
            result = ParseResult(message_type='PRIVMSG',
                                 data={},
                                 raw_message=input)
            result.is_valid = False
            result.error = str(e)
            return result

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

    