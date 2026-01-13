from ..database import DatabaseManager
from ..models import Bits
from typing import List, Optional

class BitsRepository:

    def __init__(self, db_manager:DatabaseManager):
        self.db = db_manager

    def get_by_id(self, user_id:str, room_id:str) -> Optional[List[Bits]]:
        """Get entries from bits table by user_id and room_id"""
        pass

    def save(self, bits:Bits) -> None:
        """Insert an entry into bits table"""
        
        query = '''
                INSERT INTO bits
                (user_id, room_id, timestamp, source_room_id, bits)
                VALUES (?,?,CURRENT_TIMESTAMP,?,?)
                '''
        self.db.execute_query(query, (bits.user_id,
                                      bits.room_id,
                                      bits.source_room_id,
                                      bits.bits))

    def exists(self, user_id:str, room_id:str) -> bool:
        """
        Check whether at least one entry for user_id and room_id 
        exists in bits table
        """
        query = 'SELECT 1 FROM bits WHERE user_id = ? AND room_id = ?'
        return self.db.execute_query(query, (user_id, 
                                             room_id))