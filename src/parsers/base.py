from abc import ABC, abstractmethod
from typing import Optional, Dict, Any

class ParseResult:
    def __init__(self, message_type:str, data: Dict[str, Any], raw_message:str):
        self.message_type = message_type
        self.data = data
        self.raw_message = raw_message
        self.is_valid = True
        self.error = None

class BaseParser(ABC):
    
    @abstractmethod
    def parseable(self, input:str) -> bool:
        """Checks if the parser can parse input"""
        pass

    @abstractmethod
    def parse(self, input:str) -> Optional[ParseResult]:
        """Parse the input and return structured data"""
        pass
