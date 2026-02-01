from typing import List, Optional
from ..database import DatabaseManager
from ..models import Onetapgift

class OnetapgiftRepository:

    def __init__(self, db_manager:DatabaseManager):
        self.db = db_manager
    
    def get_by_id(self, serial:int) -> Optional[Onetapgift]:
        pass

    def save(self, onetapgift:Onetapgift) -> None:
        """Insert onetapgift into onetapgift table"""

        query = '''
                INSERT INTO onetapgift
                (user_id, room_id, timestamp, tmi_sent_ts, msg_id, source_msg_id, 
                bits_spent, gift_id, user_display_name, system_msg)
                VALUES (?,?,CURRENT_TIMESTAMP,?,?,?,?,?,?,?)
                '''
        
        self.db.execute_query(query, (onetapgift.user_id,
                                      onetapgift.room_id,
                                      onetapgift.tmi_sent_ts,
                                      onetapgift.msg_id,
                                      onetapgift.source_msg_id,
                                      onetapgift.bits_spent,
                                      onetapgift.gift_id,
                                      onetapgift.user_display_name,
                                      onetapgift.system_msg))
        
    def exists(self, user_id:str, room_id:str) -> bool:
        """Checks whether user user_id ever used a onetapgift in room room_id"""

        query = 'SELECT 1 FROM onetapgift WHERE user_id = ? AND room_id = ?'
        return self.db.execute_query(query, (user_id, room_id,)) is not None