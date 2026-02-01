from typing import List, Optional
from ..database import DatabaseManager
from ..models import Paidupgrade

class PaidupgradeRepository:

    def __init__(self, db_manager:DatabaseManager):
        self.db = db_manager
        
    def get_by_id(self, serial:int) -> Optional[Paidupgrade]:
        pass

    def save(self, paidupgrade:Paidupgrade) -> None:
        """Insert a paidupgrade into paidupgrade table"""

        query = '''
                INSERT INTO paidupgrade
                (user_id, room_id, timestamp, tmi_sent_ts, msg_id, source_msg_id,
                sender_login, sender_name, sub_plan, system_msg)
                VALUES (?,?,CURRENT_TIMESTAMP,?,?,?,?,?,?,?)
                '''
        
        self.db.execute_query(query, (paidupgrade.user_id,
                                      paidupgrade.room_id,
                                      paidupgrade.tmi_sent_ts,
                                      paidupgrade.msg_id,
                                      paidupgrade.source_msg_id,
                                      paidupgrade.sender_login,
                                      paidupgrade.sender_name,
                                      paidupgrade.sub_plan,
                                      paidupgrade.system_msg))
        
    def exists(self, user_id:str, room_id:str) -> bool:
        """Checks whether user user_id ever did a paidupgrade in room room_id"""

        query = 'SELECT 1 FROM paidupgrade WHERE user_id = ? AND room_id = ?'
        return self.db.execute_query(query, (user_id, room_id,)) is not None