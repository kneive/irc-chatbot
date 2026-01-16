from .base import ParseResult
from .joinpartParser import JoinPartParser
from .messageParser import MessageParser
from .usernoticeParser import UsernoticeParser
from typing import Optional


class Saltshaker:
    def __init__(self):
        self.parsers = [JoinPartParser(),MessageParser(), UsernoticeParser()]

    def parse(self, input:str) -> Optional[ParseResult]:
        """Chooses appropriate parser and parses input"""

        for parser in self.parsers:
            if parser.parseable(input):
                return parser.parse(input)
            
        return ParseResult('UNKNOWN', {'raw': input}, input)