from typing import List, Optional
from ..database import DatabaseManager
from ..models import Sub

class SubRepository:

    def __init__(self, db_manager:DatabaseManager):
        self.db = db_manager

    def get_by_id(self, some_id:str) -> Optional[Sub]:
        pass

    def save(self, sub:Sub) -> None:
        """Inser a sub in sub table"""

        query = '''
                INSERT INTO sub
                (user_id, room_id, timestamp, tmi_sent_ts, msg_id, source_msg_id, 
                cumulative_months, months, multimonth_duration, multimonth_tenure,
                should_share_streak, sub_plan_name, sub_plan, was_gifted, system_msg)
                VALUES (?,?,CURRENT_TIMESTAMP,?,?,?,?,?,?,?,?,?,?,?,?)
                '''
        self.db.execute_query(query, (sub.user_id,
                                      sub.room_id,
                                      sub.tmi_sent_ts,
                                      sub.msg_id,
                                      sub.source_msg_id,
                                      sub.cumulative_months,
                                      sub.months,
                                      sub.multimonth_duration,
                                      sub.multimonth_tenure,
                                      sub.should_share_streak,
                                      sub.sub_plan_name,
                                      sub.sub_plan,
                                      sub.was_gifted,
                                      sub.system_msg))
        
    def exists(self, user_id:str, room_id:str) -> bool:
        """Checks whether user user_id ever had a sub in room room_id"""

        query = 'SELECT 1 FROM sub WHERE user_id = ? AND room_id = ?'
        return self.db.execute_query(query, (user_id, room_id,)) is not None