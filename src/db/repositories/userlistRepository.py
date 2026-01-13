from ..database import DatabaseManager
from ..models import UserListEntry
from typing import List, Optional

class UserlistRepository:

    def __init__(self, db_manager:DatabaseManager):
        self.db = db_manager
    
    def get_by_name(self, room_name:str, display_name:str) -> Optional[List[UserListEntry]]:
        """Get entries from userlist table by display_name and room_name"""
        pass

    def save(self, entry:UserListEntry) -> None:
        """Insert an entry into userlist table"""

        query = '''
                INSERT INTO userlist
                (room_name, display_name, join_part, timestamp)
                VALUES (?,?,?,CURRENT_TIMESTAMP)
                '''
        self.db.execute_query(query, (entry.room_name,
                                      entry.display_name,
                                      entry.join_part))
        
    def exists(self, room_name:str, display_name:str) -> bool:
        """
        Checks whether at least one entry in userlist table 
        exists for room_name + user_name
        """
        
        query = 'SELECT 1 FROM userlist WHERE room_name = ? AND display_name = ?'
        return self.db.execute_query(query, (room_name,
                                             display_name))