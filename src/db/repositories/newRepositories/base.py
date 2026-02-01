from typing import Generic, Optional, TypeVar
from abc import ABC, abstractmethod

T= TypeVar('T')

class Saltmine(Generic[T], ABC):   
    @abstractmethod
    def get_by_id(self, id:str) -> Optional[T]:
        pass

    @abstractmethod
    def save(self, entity:T) -> None:
        pass

    @abstractmethod
    def exists(self, id:str) -> bool:
        pass