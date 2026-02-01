from typing import List, Optional
from ..database import DatabaseManager
from ..models import Submystery

class SubmysteryRepository:

    def __init__(self, db_manager:DatabaseManager):
        self.db = db_manager

    def get_by_id(self, community_gift_id:str) -> Optional[Submystery]:
        pass

    def save(self, submystery:Submystery) -> None:
        """Insert a submystery into submysterygift table"""

        query = '''
                INSERT INTO submysterygift
                (user_id, room_id, timestamp, tmi_sent_ts, msg_id, source_msg_id,
                community_gift_id, contribution_type, current_contributions,
                target_contributions, user_contributions, mass_gift_count,
                origin_id, sub_plan, system_msg)
                VALUES (?,?,CURRENT_TIMESTAMP,?,?,?,?,?,?,?,?,?,?,?,?)
                '''
        
        self.db.execute_query(query, (submystery.user_id,
                                      submystery.room_id,
                                      submystery.tmi_sent_ts,
                                      submystery.msg_id,
                                      submystery.source_msg_id,
                                      submystery.community_gift_id,
                                      submystery.contribution_type,
                                      submystery.current_contributions,
                                      submystery.target_contributions,
                                      submystery.user_contributions,
                                      submystery.mass_gift_count,
                                      submystery.origin_id,
                                      submystery.sub_plan,
                                      submystery.system_msg))
        
    def exists(self, user_id:str, room_id:str) -> bool:
        """Checks whether user user_id ever gifted a submysterygift in room room_id"""

        query = 'SELECT 1 FROM submysterygift WHERE user_id = ? AND room_id = ?'
        return self.db.execute_query(query, (user_id, room_id,)) is not None