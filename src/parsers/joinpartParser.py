from .base import BaseParser, ParseResult
from typing import Optional, Dict

class JoinPartParser(BaseParser):

    def parseable(self, input:str) -> bool:
        """Check whether the input is parseable by this parser"""

        return ' JOIN ' in input or ' PART ' in input
    
    def parse(self, input:str) -> Optional[ParseResult]:
        """Parse input and return ParseResult or None"""

        try:
            tags = {}
            if ' JOIN ' in input:
                type = 'JOIN'
            else:
                type = 'PART'

            if ' JOIN ' in input:    
                return ParseResult('JOIN',
                                   self._parseJoin(input),
                                   input)
            
            else:
                return ParseResult('PART', 
                                   self._parsePart(input), 
                                   input)
        
        except Exception as e:
            print(input)
            print(f'(parse) {type} message is corrupted: {e.with_traceback}, ({tags})' )
            result = ParseResult(type, {}, input)
            result.is_valid = False
            result.error = str(e)

    def _parseJoin(self, input:str) -> Dict[str,str]:
        """Parse JOIN message"""

        tags = {}
        
        tags['msg-type'] = 'JOIN'
                
        idx = input.find('!')
        if idx == -1:
            raise ValueError("(_parseJoin) JOIN message is corrupted: no '!'")

        tags['display-name'] = input[1:idx]

        idx = input.find('JOIN #')
        if idx == -1:
            raise ValueError("(_parseJoin) JOIN messaee is corrupted: no '#'")

        tags['room-name'] = input[idx+1:].strip()

        return tags
    
    def _parsePart(self, input:str) -> Dict[str,str]:
        """Parse PART message"""

        tags = {}

        tags['msg-type'] = 'PART'
                
        idx = input.find('!')
        if idx == -1:
            raise ValueError("(_parsePart) PART message is corrupted: no '!'")

        tags['display-name'] = input[1:idx]

        idx = input.find('PART #')
        if idx == -1:
            raise ValueError("(_parsePart) PART messaee is corrupted: no '#'")

        tags['room-name'] = input[idx+1:].strip()

        return tags