from .base import BaseParser, ParseResult
from .tags.tagFactory import TagFactory
from typing import Optional, Dict
import traceback

class RoomstateParser(BaseParser):

    def parseable(self, input:str) -> bool:
        """Check whether the input is parseable"""

        return ' ROOMSTATE ' in input
    
    def parse(self, input:str) -> Optional[ParseResult]:
        """Parse input and return ParseResult or None"""

        try:
            end = input.find(' :tmi.twitch.tv')
            if end == -1:
                raise ValueError("(pares) USERNOTICE message is corrupted: no ' :'")

            raw_tags = self._parseTags(input[1:end])

            tags = TagFactory.createRoomstateTag(raw_tags)

            return ParseResult(message_type='ROOMSTATE',
                               data=tags,
                               raw_message=input)

        except Exception as e:
            print(input)
            print(f'(parse) ROOMSTATE message is corrupted: {e} ({tags})')
            print(f'Traceback: {traceback.format_exc()}')
            result = ParseResult(message_type='ROOMSTATE',
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
            raise ValueError(f'(_parseTags) ROOMSTATE message is corrupted {tags.items()}')