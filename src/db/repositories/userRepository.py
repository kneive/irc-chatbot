from typing import Optional, List
from ..database import DatabaseManager
from ..models import User
from .base import Saltmine

class UserRepository(Saltmine[User]):
    def __init__(self, db_manager:DatabaseManager):
        self.db = db_manager

    def get_by_id(self, user_id:str) -> Optional[User]:
        pass

    def save(self, user:User) -> None:
        pass

    def exists(self, user_id:str) -> bool:
        pass