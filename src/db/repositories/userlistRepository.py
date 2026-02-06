from typing import List, Optional
from ..database import DatabaseManager
from ..models import Userlist

class UserlistRepository:

    def __init__(self, db_manager:DatabaseManager):
        self.db = db_manager

    def get_by_id(self, seriall:int) -> Optional[Userlist]:
        pass

    def save(self, userlist:Userlist) -> None:
        """Insert a userlist into userlist table"""

        query = '''
                INSERT INTO userlist
                (timestamp, room_name, room_id, username, join_part)
                VALUES (CURRENT_TIMESTAMP,?,?,?,?)
                '''
        
        self.db.execute_query(query, (userlist.room_name,
                                      userlist.room_id,
                                      userlist.username,
                                      userlist.join_part))
        
    def exists(self, room_name:str, username:str) -> bool:
        """Checks whether user username ever appeared in room room_name"""

        query = 'SELECT 1 FROM userlist WHERE room_name = ? AND username = ?'
        return self.db.execute_query(query, (room_name, username,)) is not None