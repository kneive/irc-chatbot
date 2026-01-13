from .base import BaseParser, ParseResult
from typing import Optional, Dict

class MessageParser(BaseParser):

    def parseable(self, input:str) -> bool:
        """Check whether the input is parseable by this parser"""
        
        return ' PRIVMSG ' in input
    
    def parse(self, input:str) -> Optional[ParseResult]:
        """Parse input and return ParseResult or None"""

        pass


    def _parseTags(self, input:str) -> Dict[str, str]:
        """Parse message tags from input string"""

        pass