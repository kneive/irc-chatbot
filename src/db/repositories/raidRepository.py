from ..database import DatabaseManager
from ..models import Raid
from typing import List, Optional

class RaidRepository:

    def __init__(self, db_manager:DatabaseManager):
        self.db = db_manager

    def get_by_id(self, user_id:str, room_id:str) -> Optional[List[Raid]]:
        """Get entries from raid table by user_id and room_id"""
        pass

    def save(self, raid:Raid) -> None:
        """Insert an entry into raid table"""
        
        query = '''
                INSERT INTO raid
                (room_id, user_id, timestamp, source_room_id, viewer_count)
                VALUES (?,?,CURRENT_TIMESTAMP,?,?)
                '''
        self.db.execute_query(query, (raid.room_id,
                                      raid.user_id,
                                      raid.source_room_id,
                                      raid.viewer_count))

    def exists(self, user_id:str, room_id:str) -> bool:
        """
        Check whether at least one entry for user_id and room_id 
        exists in raid table
        """
        
        query = 'SELECT 1 FROM raid WHERE user_id = ? AND room_id = ?'
        return self.db.execute_query(query, (user_id, room_id,)) is not None