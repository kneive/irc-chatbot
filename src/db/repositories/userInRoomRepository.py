from typing import Optional, List
from ..database import DatabaseManager
from ..models import UserInRoom

class UserInRoomRepository:

    def __init__(self, db_manager:DatabaseManager):
        self.db = db_manager

    def get_by_id(self, room_id:str, user_id:str) -> Optional[UserInRoom]:
        pass

    def save(self, user_in_room:UserInRoom) -> None:
        pass

    def exists(self, room_id:str, user_id:str) -> bool:
        pass