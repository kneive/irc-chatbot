from typing import Optional, List
from ..database import DatabaseManager
from ..models import User
from .base import Saltmine

class UserRepository(Saltmine[User]):
    def __init__(self, db_manager:DatabaseManager):
        self.db = db_manager

    def get_by_id(self, user_id:str) -> Optional[User]:
        """Get entry for user_id from user table"""

        query = '''
                SELECT user_id, display_name, username, color, turbo
                FROM user
                WHERE user_id = ?
                '''
        entry = self.db.execute_query(query, (user_id))
        
        if entry:
            return User(user_id=entry[0],
                        display_name=entry[1],
                        username=entry[2],
                        color=entry[3],
                        turbo=entry[4])
        return None

    def save(self, user:User) -> None:
        """Insert or update a user in user table"""

        query = '''
                INSERT OR REPLACE INTO user
                (user_id, display_name, username, color, turbo, added)
                VALUES (?,?,?,?,?, CURRENT_TIMESTAMP)
                '''
        self.db.execute_query(query, (user.user_id, 
                                      user.display_name, 
                                      user.username, 
                                      user.color, 
                                      user.turbo))

    def exists(self, user_id:str) -> bool:
        """Check whether user_id exists in user table"""

        query = 'SELECT 1 FROM user WHERE user_id = ?'
        return self.db.execute_query(query, (user_id,)) is not None
        