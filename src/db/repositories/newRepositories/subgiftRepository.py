from typing import List, Optional
from ..database import DatabaseManager
from ..models import Subgift

class SubgiftRepository:

    def __init__(self, db_manager:DatabaseManager):
        self.db = db_manager

    def get_by_id(self, origin_id:str) -> Optional[Subgift]:
        pass

    def save(self, subgift:Subgift) -> None:
        """Insert a subgift into subgift table"""

        query = '''
                INSERT INTO subgift
                (user_id, room_id, timestamp, tmi_sent_ts, msg_id, source_msg_id, 
                community_gift_id, fun_string, gift_months, months, origin_id, 
                recipient_id, recipient_display_name, recipient_user_name, 
                sender_count, sub_plan_name, sub_plan, system_msg)
                VALUES (?,?, CURRENT_TIMESTAMP,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                '''
        
        self.db.execute_query(query, (subgift.user_id,
                                      subgift.room_id,
                                      subgift.tmi_sent_ts,
                                      subgift.msg_id,
                                      subgift.source_msg_id,
                                      subgift.community_gift_id,
                                      subgift.fun_string,
                                      subgift.gift_months,
                                      subgift.months,
                                      subgift.origin_id,
                                      subgift.recipient_id,
                                      subgift.recipient_display_name,
                                      subgift.recipient_user_name,
                                      subgift.sender_count,
                                      subgift.sub_plan_name,
                                      subgift.sub_plan,
                                      subgift.system_msg))
        

    def exists(self, user_id:str, room_id:str) -> bool:
        """Checks whether user user_id ever recieved a subgift in room room_id)"""

        query = 'SELECT 1 FROM subgift WHERE user_id = ? AND room_id = ?'
        return self.db.execute_query(query,  (user_id, room_id,)) is not None