from typing import Optional
from ..database import DatabaseManager
from ..models import Bits

class BitsRepository:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def get_by_id(self, message_id: str) -> Optional[Bits]:
        pass

    def save(self, bits: Bits) -> None:
        """Insert into bits table"""

        query = '''
                INSERT INTO bits (
                user_id, room_id, source_room_id, timestamp, bits)
                VALUES (?,?,?,CURRENT_TIMESTAMP,?)
                '''
        self.db.execute_query(query, (bits.user_id, bits.room_id, bits.source_room_id, bits.bits))

    def exists(self, user_id:str, room_id:str) -> bool:
        """Checks whether user user_id ever sent bits in room room_id"""

        query = 'SELECT 1 FROM bits WHERE user_id = ? AND room_id = ?'
        return self.db.execute_query(query, (user_id, room_id,)) is not None