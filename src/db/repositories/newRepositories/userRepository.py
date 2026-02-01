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
                SELECT user_id, login, display_name, user_type, turbo, created
                FROM user
                WHERE user_id = ?
                '''
        entry = self.db.execute_query(query, (user_id))
        
        if entry:
            return User(user_id=entry[0],
                        login=entry[1],
                        display_name=entry[2],
                        username=entry[3],
                        user_type=entry[4],
                        turbo=entry[5],
                        created=entry[6])
        return None

    def save(self, user:User) -> None:
        """Insert or update a user in user table"""

        query = '''
                INSERT OR REPLACE INTO user
                (user_id, login, display_name, user_type, turbo, created)
                VALUES (?,?,?,?,?, CURRENT_TIMESTAMP)
                '''
        self.db.execute_query(query, (user.user_id, 
                                      user.login,
                                      user.display_name,  
                                      user.user_type,
                                      user.turbo))

    def exists(self, user_id:str) -> bool:
        """Check whether user_id exists in user table"""

        query = 'SELECT 1 FROM user WHERE user_id = ?'
        return self.db.execute_query(query, (user_id,)) is not None
        