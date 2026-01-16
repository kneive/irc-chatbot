from typing import Optional, List
from ..database import DatabaseManager
from ..models import ViewerMilestone
from .base import Saltmine

class ViewerMilestoneRepository(Saltmine[ViewerMilestone]):

    def __init__(self, db_manager:DatabaseManager):
        self.db = db_manager
    
    def get_by_id(self, room_id:str, user_id:str) -> List[ViewerMilestone]:
        """Get viewer milestones for a given room_id by a given user_id"""

        pass

    def save(self, milestone:ViewerMilestone) -> None:
        """Insert a viewer milestone into viewermilestone table"""

        query = '''
                INSERT INTO viewermilestone
                (room_id, user_id, display_name, timestamp, streak)
                VALUES (?,?,?,CURRENT_TIMESTAMP,?)
                '''
        
        self.db.execute_query(query, (milestone.room_id,
                                      milestone.user_id,
                                      milestone.display_name,
                                      milestone.streak))

    def exists(self, room_id:str, user_id:str) -> bool:
        """Check whether a viewer milestone was ever shared by user_id in room_id"""

        query = 'SELECT 1 FROM viewermilestone WHERE room_id = ? AND user_id = ?'
        return self.db.execute_query(query, (room_id, user_id,)) is not None