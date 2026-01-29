import sqlite3
from typing import List, Optional

class DatabaseManager:
    def __init__(self, db_path='saltmine.db'):
        self.db_path = db_path
        self.setup_database()

    def setup_database(self):
        """Create all tables"""
        with sqlite3.connect(self.db_path) as conn:
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS user (
                    user_id TEXT PRIMARY KEY,
                    login TEXT DEFAULT '',
                    display_name TEXT DEFAULT '',
                    user_type TEXT DEFAULT '',
                    turbo INTEGER DEFAULT 0
                )
            ''')

            conn.execute('''
                CREATE TABLE IF NOT EXISTS room (
                    room_id TEXT PRIMARY KEY,
                    room_name TEXT DEFAULT '#UNKNOWN')
            ''')

            conn.execute('''
                CREATE TABLE IF NOT EXISTS user_room (
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP PRIMARY KEY,
                    user_id TEXT FOREIGN KEY REFERENCES user (user_id),
                    room_id TEXT FOREIGN KEY REFERENCES room (room_id),
                    badges TEXT DEFAULT '',
                    badge_info TEXT DEFAULT '',
                    subscriber INTEGER DEFAULT 0,
                    sub_streak INTEGER DEFAULT 0,
                    vip INTEGER DEFAULT 0,
                    mod INTEGER DEFAULT 0)
            ''')

            conn.execute('''
                CREATE TABLE IF NOT EXISTS privmsg (
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ,
                    tmi_sent_ts TEXT NOT NULL,
                    id TEXT PRIMARY KEY,
                    source_id TEXT,
                    room_id TEXT FOREIGN KEY REFERENCES room (room_id),
                    source_room_id TEXT DEFAULT 'NULL',
                    user_id TEXT FOREIGN KEY REFERENCES user (user_id),
                    color TEXT DEFAULT '',
                    returning_chatter INTEGER DEFAULT 0,
                    first_msg INTEGER DEFAULT 0,
                    flags TEXT DEFAULT '',
                    emotes TEXT DEFAULT '',
                    msg_content TEXT DEFAULT '',
                )
            ''')

            conn.execute('''
                CREATE TABLE IF NOT EXISTS raid (
                    user_id TEXT FOREIGN KEY REFERENCES user (user_id),
                    rooom_id TEXT FOREIGN KEY REFERENCES room (room_id),
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    tmi_sent_ts TEXT NOT NULL,
                    msg_id TEXT NOT NULL,
                    msg_param_displayName TEXT,
                    msg_param_login TEXT,
                    msg_param_profileImageURL TEXT,
                    msg_param_viewerCount TEXT,
                    system_msg TEXT NOT NULL
                )
            ''')


        #TODO Raids, Subs, submystery, raids, announcements, bits


    def execute_query(self, query:str, params:tuple=()) -> Optional[tuple]:
        """Execute a query against the database and return one result"""

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(query, params)
                return cursor.fetchone()
        except Exception as e:
            print(f"Database query error: {e}")
            return None
        
    def execute_query_all(self, query:str, params:tuple=()) -> List[tuple]:
        """Execute a query againt the database and return all results"""

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(query, params)
                return cursor.fetchall()
        except Exception as e:
            print(f"Database query error: {e}")
            return []