from typing import Optional, List
from ..database import DatabaseManager
from ..models import UserInRoom

class UserInRoomRepository:

    def __init__(self, db_manager:DatabaseManager):
        self.db = db_manager

    def get_by_id(self, room_id:str, user_id:str) -> Optional[UserInRoom]:
        pass

    def save(self, user_in_room:UserInRoom) -> None:
        """Insert or update a user in user_in_room table"""

        query = '''
                INSERT OR REPLACE INTO user_in_room
                (room_id, user_id, last_seen, returning_chatter, 
                first_message, sub, vip, mod, badges, user_type)
                VALUES (?,?, CURRENT_TIMESTAMP,?,?,?,?,?,?,?)
                '''
        self.db.execute_query(query, (UserInRoom.room_id,
                                      UserInRoom.user_id,
                                      UserInRoom.returning_chatter,
                                      UserInRoom.first_message,
                                      UserInRoom.sub,
                                      UserInRoom.vip,
                                      UserInRoom.mod,
                                      UserInRoom.badges,
                                      UserInRoom.user_type))

    def exists(self, room_id:str, user_id:str) -> bool:
        """Checks whether a user_id is present in user_in_room table"""

        query = 'SELECT 1 FROM user_in_room WHERE room_id = ? AND user_id = ?'
        return self.db.execute_query(query(room_id, user_id))