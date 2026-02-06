from typing import List, Optional
from ..database import DatabaseManager
from ..models import Bitsbadgetier

class BitsbadgetierRepository:

    def __init__(self, db_manager:DatabaseManager):
        self.db=db_manager

    def get_by_id(self, serial:int) -> Optional[Bitsbadgetier]:
        pass

    def save(self, bitsbadge:Bitsbadgetier) -> None:
        """Insert bitsbadgetier into bitsbadgetier table"""

        query = '''
                INSERT INTO bitsbadgetier
                (room_id, user_id, timestamp, msg_param_threshold, system_msg)
                VALUES (?,?,CURRENT_TIMESTAMP,?,?)
                '''
        
        self.db.execute_query(query, (bitsbadge.room_id,
                                      bitsbadge.user_id,
                                      bitsbadge.msg_param_threshold,
                                      bitsbadge.system_msg))
        
    def exists(self, user_id:str, room_id:str) -> bool:
        """Checks whether user user_id ever bought a bitsbadge in room room_id"""

        query = 'SELECT 1 FROM bitsbadgetier WHERE user_id = ? AND room_id = ?'
        return self.db.execute_query(query, (user_id, room_id,)) is not None