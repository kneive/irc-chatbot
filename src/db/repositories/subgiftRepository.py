from ..database import DatabaseManager
from ..models import Subgift
from typing import List

class SubgiftRepository:

    def __init__(self, db_manager:DatabaseManager):
        self.db = db_manager

    def get_by_id(self, gift_id:str) -> Subgift:
        """Get a subgift by gift_id from subgift table"""
        pass

    def save(self, subgift:Subgift) -> None:
        """Insert an entry into subgift table"""
        
        query = '''
                INSERT INTO subgift
                (user_id, room_id, timestamp, gift_id, gift_count, gifter_total, 
                sub_plan)
                VALUES (?,?,CURRENT_TIMESTAMP,?,?,?,?)
                '''
        self.db.execute_query(query, (subgift.user_id,
                                      subgift.room_id,
                                      subgift.gift_id,
                                      subgift.gift_count,
                                      subgift.gifter_total,
                                      subgift.sub_plan))

    def exists(self, gift_id:str) -> bool:
        """Check whether an entry for gift_id exists in subgift table"""

        query = 'SELECT 1 FROM subgift WHERE gift_id = ?'
        return self.db.execute_query(query, (gift_id,)) is not None