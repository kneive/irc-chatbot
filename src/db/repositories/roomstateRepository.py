from ..database import DatabaseManager
from ..models import Roomstate
from typing import List, Optional

class RoomStateRepository:

    def __init__(self, db_manager:DatabaseManager):
        self.db = db_manager

    def get_by_id(self, room_id:str) -> Optional[Roomstate]:
        """Get the state of a room by room_id from roomstate table"""
        
        query = '''
                SELECT room_id, timestamp, follow_only, sub_only, emote_only, 
                       slow_mode, r9k
                FROM roomstate
                WHERE room_id = ?
                '''
        
        entry = self.db.execute_query(query, (room_id))

        if entry:
            return Roomstate(room_id=entry[0],
                             timestamp=entry[1],
                             followers_only=entry[2],
                             sub_only=entry[3],
                             emote_only=entry[4],
                             slow_mode=entry[5],
                             r9k=entry[6])
        return None

    def save(self, roomstate:Roomstate) -> None:
        """Insert or update an entry in roomstate table"""
        
        query = '''
                INSERT OR REPLACE INTO roomstate
                (room_id, timestamp, followers_only, sub_only, emote_only, 
                slow_mode, r9k)
                VALUES (?,CURRENT_TIMESTAMP,?,?,?,?,?)
                '''
        self.db.execute_query(query, (roomstate.room_id,
                                      roomstate.followers_only,
                                      roomstate.sub_only,
                                      roomstate.emote_only,
                                      roomstate.slow_mode,
                                      roomstate.r9k))

    def exists(self, room_id:str) -> bool:
        """Check whether room_id exists in roomstate table"""
        
        query = 'SELECT 1 FROM roomstate WHERE room_id = ?'
        return self.db.execute_query(query, (room_id,)) is not None