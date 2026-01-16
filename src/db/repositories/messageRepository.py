from typing import Optional, List
from ..database import DatabaseManager
from ..models import MessageInRoom
from .base import Saltmine

class MessageRepository(Saltmine[MessageInRoom]):

    def __init__(self, db_manager:DatabaseManager):
        self.db = db_manager

    def get_by_id(self, message_id:str) -> Optional[MessageInRoom]:
        pass

    def get_by_id(self, room_id:str, user_id:str) -> Optional[List[MessageInRoom]]:
        pass

    def save(self, message:MessageInRoom) -> None:
        """Insert a message into message_in_room table"""

        query = '''
                INSERT INTO message_in_room
                (message_id, room_id, user_id, timestamp, reply_message_id,
                reply_user_id, reply_display_name, thread_message_id,
                thread_user_id, thread_display_name)
                VALUES (?,?,?,CURRENT_TIMESTAMP,?,?,?,?,?,?)
                '''
        self.db.execute_query(query, (message.message_id,
                                      message.room_id,
                                      message.user_id,
                                      message.reply_message_id,
                                      message.reply_user_id,
                                      message.reply_display_name,
                                      message.thread_message_id,
                                      message.thread_user_id,
                                      message.thread_display_name))

    def exists(self, message_id:str) -> bool:
        """Checks whether message_id exists in message_in_room table"""

        query = 'SELECT 1 FROM message_in_room WHERE message_id = ?'
        return self.db.execute_query(query, (message_id,)) is not None



