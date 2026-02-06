from typing import List, Optional
from ..database import DatabaseManager
from ..models import Raid

class RaidRepository:

    def __init__(self, db_manager:DatabaseManager):
        self.db = db_manager

    def get_by_id(self, user_id:str, room_id:str) -> Optional[List[Raid]]:
        """Get entries from raid table by user_id and room_id"""
        pass

    def save(self, raid:Raid) -> None:
        """Insert an entry into raid table"""
        
        query = '''
                INSERT INTO raid
                (user_id, room_id, source_room_id, timestamp, tmi_sent_ts, msg_id, source_msg_id, 
                msg_param_displayName, msg_param_login, msg_param_profileImageURL,
                 msg_param_viewerCount, system_msg)
                VALUES (?,?,?,CURRENT_TIMESTAMP,?,?,?,?,?,?,?,?)
                '''
        self.db.execute_query(query, (raid.user_id,
                                      raid.room_id,
                                      raid.source_room_id,
                                      raid.tmi_sent_ts,
                                      raid.msg_id,
                                      raid.source_msg_id,
                                      raid.msg_param_displayName,
                                      raid.msg_param_login,
                                      raid.msg_param_profileImageURL,
                                      raid.msg_param_viewerCount,
                                      raid.system_msg))

    def exists(self, user_id:str, room_id:str) -> bool:
        """
        Check whether at least one entry for user_id and room_id 
        exists in raid table
        """
        
        query = 'SELECT 1 FROM raid WHERE user_id = ? AND room_id = ?'
        return self.db.execute_query(query, (user_id, room_id,)) is not None