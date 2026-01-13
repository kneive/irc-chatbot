from typing import List
from ..database import DatabaseManager
from ..models import Sub

class SubRepository:

    def __init__(self, db_manager:DatabaseManager):
        self.db = db_manager

    def get_by_id(self, room_id:str, user_id:str) -> List[Sub]:
        pass

    def save(self, sub:Sub) -> None:
        """Insert an entry into subs table"""

        query = '''
                INSERT INTO subs
                (user_id, room_id, timestamp, message_id, gift_id, sub_plan,
                months, gift_months, multimonth_duration, multimonth_tenure,
                streak_months, share_streak, cumulative)
                VALUES (?,?,CURRENT_TIMESTAMP,?,?,?,?,?,?,?,?,?,?)
                '''
        self.db.execute_query(query, (sub.user_id,
                                      sub.room_id,
                                      sub.message_id,
                                      sub.gift_id,
                                      sub.sub_plan,
                                      sub.months,
                                      sub.gift_months,
                                      sub.multimonth_duration,
                                      sub.multimonth_tenure,
                                      sub.streak_months,
                                      sub.share_streak,
                                      sub.cumulative))

    def exists(self, room_id:str, user_id:str) -> bool:
        """Checks whether at leas one entry in subs table exists for 
        room_id and user_id"""

        query = 'SELECT 1 FROM subs WHERE room_id = ? AND user_id = ?'
        return self.db.execute_query(query, (room_id, user_id))