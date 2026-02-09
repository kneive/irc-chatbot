from typing import List, Optional
from ..database import DatabaseManager
from ..models import Roomstate

class RoomStateRepository:

    def __init__(self, db_manager:DatabaseManager):
        self.db = db_manager

    def get_by_id(self, room_id:str) -> Optional[Roomstate]:
        """Get the state of a room by room_id from roomstate table"""
        
        query = '''
                SELECT timestamp, room_id, emote_only, followers_only, r9k,
                       slow, subs_only
                FROM roomstate
                WHERE room_id = ?
                '''
        
        entry = self.db.execute_query(query, (room_id,))

        if entry:
            return Roomstate(timestamp=entry[0],
                             room_id=entry[1],
                             emote_only=entry[2],
                             followers_only=entry[3],
                             r9k=entry[4],
                             slow_mode=entry[5],
                             sub_only=entry[6])
        return None

    def save(self, roomstate:Roomstate) -> None:
        """Insert or update an entry in roomstate table"""
        
        query = '''
                INSERT OR REPLACE INTO roomstate
                (timestamp, room_id, emote_only, followers_only, r9k, slow, 
                subs_only)
                VALUES (CURRENT_TIMESTAMP,?,?,?,?,?,?)
                '''
        self.db.execute_query(query, (roomstate.room_id,
                                      roomstate.emote_only,
                                      roomstate.followers_only,
                                      roomstate.r9k,
                                      roomstate.slow_mode,
                                      roomstate.sub_only))

    def exists(self, room_id:str) -> bool:
        """Check whether room_id exists in roomstate table"""
        
        query = 'SELECT 1 FROM roomstate WHERE room_id = ?'
        return self.db.execute_query(query, (room_id,)) is not None