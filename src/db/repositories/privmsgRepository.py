from typing import Optional, List
from ..database import DatabaseManager
from ..models import Privmsg

class PrivmsgRepository:

    def __init__(self, db_manager:DatabaseManager):
        self.db = db_manager

    def get_by_id(self, message_id:str) -> Optional[Privmsg]:
        pass

    def save(self, privmsg:Privmsg) -> None:
        """Insert a privmsg into privmsg table"""

        query = '''
                INSERT INTO privmsg
                (timestamp, tmi_sent_ts, message_id, source_message_id, room_id, 
                source_room_id, user_id, color, returning_chatter, first_msg, 
                flags, emotes, msg_content)
                VALUES (CURRENT_TIMESTAMP,?,?,?,?,?,?,?,?,?,?,?,?)
                '''
        self.db.execute_query(query, (privmsg.tmi_sent_ts,
                                      privmsg.message_id,
                                      privmsg.source_message_id,
                                      privmsg.room_id,
                                      privmsg.source_room_id,
                                      privmsg.user_id,
                                      privmsg.color,
                                      privmsg.returning_chatter,
                                      privmsg.first_msg,
                                      privmsg.flags,
                                      privmsg.emotes,
                                      privmsg.msg_content))
        
    def exists(self, user_id:str, room_id:str) -> bool:
        """Checks whether a user user_id has ever posted a message in room room_id"""

        query = 'SELECT 1 FROM privmsg WHERE user_id = ? AND room_id = ?'
        return self.db.execute_query(query, (user_id, room_id,)) is not None