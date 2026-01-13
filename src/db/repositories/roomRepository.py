from typing import Optional, List
from ..database import DatabaseManager
from ..models import Room
from .base import Saltmine

class RoomRepository(Saltmine[Room]):

    def __init__(self, db_manager:DatabaseManager):
        self.db = db_manager

    def get_by_id(self, room_id:str) -> Optional[Room]:
        pass

    def save(self, room:Room) -> None:
        pass

    def exists(self, room_id:str) -> bool:
        pass