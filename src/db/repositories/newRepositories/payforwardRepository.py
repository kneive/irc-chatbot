from typing import List, Optional
from ..database import DatabaseManager
from ..models import Payforward

class PayforwardRepository:

    def __init__(self, db_manager:DatabaseManager):
        self.db = db_manager

    def get_by_id(self, serial:int) -> Optional[Payforward]:
        pass

    def save(self, payforward:Payforward) -> None:
        """Insert a payforward into payforward table"""

        query = '''
                INSERT INTO payforward
                (user_id, room_id, timestamp, tmi_sent_ts, msg_id, source_msg_id,
                prior_gifter_anonymous, prior_gifter_id, prior_gifter_display_name,
                prior_gifter_user_name, recipient_id, recipient_display_name,
                recipient_user_name, system_msg)
                VALUES (?,?,CURRENT_TIMESTAMP,?,?,?,?,?,?,?,?,?,?,?)
                '''
        
        self.db.execute_query(query, (payforward.user_id,
                                      payforward.room_id,
                                      payforward.tmi_sent_ts,
                                      payforward.msg_id,
                                      payforward.source_msg_id,
                                      payforward.prior_gifter_anonymous,
                                      payforward.prior_gifter_id,
                                      payforward.prior_gifter_display__name,
                                      payforward.prior_gifter_user_name,
                                      payforward.recipient_id,
                                      payforward.recipient_display_name,
                                      payforward.recipient_user_name,
                                      payforward.system_msg))

    def exists(self, user_id:str, room_id:str) -> bool:
        """Checks whether user user_id ever used a payforward in room room_id"""

        query = 'SELECT 1 FROM payforward WHERE user_id = ? AND room_id = ?'
        return self.db.execute_query(query, (user_id, room_id,)) is not None