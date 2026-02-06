from typing import Optional, List
from ..database import DatabaseManager
from ..models import UserRoom

class UserRoomRepository:

    def __init__(self, db_manager:DatabaseManager):
        self.db = db_manager

    def get_by_id(self, room_id:str, user_id:str) -> Optional[UserRoom]:
        pass

    def save(self, user_in_room:UserRoom) -> None:
        """Insert or update a user in user_in_room table"""

        query = '''
                INSERT OR REPLACE INTO user_in_room
                (timestamp, user_id, room_id, badges, 
                badge_info, subscriber, sub_streak, vip, mod)
                VALUES (CURRENT_TIMESTAMP,?,?,?,?,?,?,?,?)
                '''
        self.db.execute_query(query, (user_in_room.user_id,
                                      user_in_room.room_id,
                                      user_in_room.badges,
                                      user_in_room.badge_info,
                                      user_in_room.subscriber,
                                      user_in_room.sub_streak,
                                      user_in_room.vip,
                                      user_in_room.mod))

    def exists(self, room_id:str, user_id:str) -> bool:
        """Checks whether a user_id is present in user_in_room table"""
        
        query = 'SELECT 1 FROM user_in_room WHERE room_id = ? AND user_id = ?'
        return self.db.execute_query(query, (room_id, user_id,)) is not None