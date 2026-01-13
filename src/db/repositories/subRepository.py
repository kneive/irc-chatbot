from typing import List
from ..database import DatabaseManager
from ..models import Sub

class SubRepository:

    def __init__(self, db_manager:DatabaseManager):
        self.db = db_manager

    def get_by_id(self, room_id:str, user_id:str) -> List[Sub]:
        pass

    def save(self, sub:Sub) -> None:
        pass

    def exists(self, room_id:str, user_id:str) -> bool:
        pass