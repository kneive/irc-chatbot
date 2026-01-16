from typing import Optional, List
from ..database import DatabaseManager
from ..models import Announcement
from .base import Saltmine

class AnnouncementRepository(Saltmine[Announcement]):

    def __init__(self, db_manager:DatabaseManager):
        self.db = db_manager

    def get_by_id(self, room_id:str, user_id:str) -> List[Announcement]:
        """Get announcements for a given room_id by a given user_id"""

        pass

    def save(self, announcement:Announcement) -> None:
        """Insert an announcement into announcement table"""

        query = '''
                INSERT INTO announcement
                (room_id, user_id, display_name, timestamp, msg_content)
                VALUES (?,?,?,CURRENT_TIMESTAMP,?)
                '''
        
        self.db.execute_query(query,(announcement.room_id,
                                     announcement.user_id,
                                     announcement.display_name,
                                     announcement.msg_content))
        
    def exists(self, room_id:str, user_id:str) -> bool:
        """Check whether an announcement was ever made by user_id in room_id"""

        query = 'SELECT 1 FROM announcement WHERE room_id = ? AND user_id = ?'
        return self.db.execute_query(query, (room_id, user_id,)) is not None