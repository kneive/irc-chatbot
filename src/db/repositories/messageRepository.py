from typing import Optional, List
from ..database import DatabaseManager
from ..models import MessageInRoom
from .base import Saltmine

class MessageRepository(Saltmine[MessageInRoom]):

    def __init__(self, db_manager:DatabaseManager):
        self.db = db_manager

    def get_by_id(self, message_id:str) -> Optional[MessageInRoom]:
        pass

    def get_by_id(self, room_id:str, user_id:str) -> Optional[List[MessageInRoom]]:
        pass

    def save(self, message:MessageInRoom) -> None:
        pass

    def exists(self, message_id:str) -> bool:
        pass


