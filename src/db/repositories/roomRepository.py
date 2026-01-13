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
        """Insert or update a room in room table"""

        query = '''
                INSERT OR REPLACE INTO room 
                (room_id, room_name, added) 
                VALUES (?,?, CURRENT_TIMESTAMP)
                '''
        self.db.execute_query(query, (Room.room_id, 
                                      Room.room_name))

    def exists(self, room_id:str) -> bool:
        """Checks whether room_id exists in room table"""

        query= 'SELECT 1 FROM room WHERE id = ?'
        return self.db.execute_query(query, (room_id))