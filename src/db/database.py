import sqlite3
from typing import Optional, List

class DatabaseManager:
    def __init__(self, db_path='saltmine.db'):
        self.db_path = db_path
        self.setup_database()

    def setup_database(self):
        """Create all tables for the database"""
        with sqlite3.connect(self.db_path) as conn:

            conn.execute('''
                CREATE TABLE IF NOT EXISTS bits (
                    user_id TEXT,
                    room_id TEXT,
                    timestamp TIMESTAMP,
                    source_room_id TEXT,
                    bits INTEGER DEFAULT 0,
                    FOREIGN KEY (room_id) REFERENCES room (id),
                    FOREIGN KEY (user_id) REFERENCES user (id)
                )
            ''')

            conn.execute('''
                CREATE TABLE IF NOT EXISTS message_in_room (
                    message_id TEXT PRIMARY KEY,
                    room_id TEXT,
                    user_id TEXT,
                    timestamp TIMESTAMP,
                    reply_message_id TEXT,
                    reply_user_id TEXT,
                    reply_display_name TEXT,
                    thread_message_id TEXT,
                    thread_user_id TEXT,
                    thread_display_name TEXT,
                    FOREIGN KEY (room_id) REFERENCES room (id),
                    FOREIGN KEY (user_id) REFERENCES user (id)
                )
            ''')

            conn.execute('''
                CREATE TABLE IF NOT EXISTS raid (
                    room_id TEXT,
                    user_id TEXT,
                    timestamp TIMESTAMP,
                    source_room_id TEXT,
                    viewer_count INTEGER DEFAULT 0,
                    FOREIGN KEY (room_id) REFERENCES room (id),
                    FOREIGN KEY (user_id) REFERENCES user (id)
                )
            ''')

            conn.execute('''
                CREATE TABLE IF NOT EXISTS room (
                    room_id TEXT PRIMARY KEY,
                    room_name TEXT NOT NULL,
                    added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )             
            ''')

            conn.execute('''
                CREATE TABLE IF NOT EXISTS roomstate (
                    room_id TEXT PRIMARY KEY,
                    timestamp TIMESTAMP,
                    follow_only INTEGER DEFAULT 0,
                    sub_only INTEGER DEFAULT 0,
                    emote_only INTEGER DEFAULT 0,
                    slow_mode INTEGER DEFAULT 0,
                    r9k INTEGER DEFAULT 0,
                    FOREIGN KEY (room_id) REFERENCES room (id))
            ''')

            conn.execute('''
                CREATE TABLE IF NOT EXISTS subs (
                    user_id TEXT,
                    room_id TEXT,
                    timestamp TIMESTAMP,
                    message_id TEXT,
                    gift_id TEXT,
                    sub_plan TEXT,
                    months INTEGER DEFAULT 0,
                    gift_months INTEGER DEFAULT 0,
                    multimonth_duration INTEGER DEFAULT 0,
                    multimonth_tenure INTEGER DEFAULT 0,
                    streak_months INTEGER DEFAULT 0,
                    share_streak INTEGER DEFAULT 0,
                    cumulative INTEGER DEFAULT 0,
                    FOREIGN KEY (room_id) REFERENCES room (id),
                    FOREIGN KEY (user_id) REFERENCES user (id)
                )
            ''')

            conn.execute('''
                CREATE TABLE IF NOT EXISTS subgift (
                    user_id TEXT,
                    room_id TEXT,
                    timestamp TIMESTAMP,
                    gift_id TEXT PRIMARY KEY,
                    gift_count INTEGER DEFAULT 0,
                    gifter_total INTEGER DEFAULT 0,
                    sub_plan TEXT,
                    FOREIGN KEY (room_id) REFERENCES room (id),
                    FOREIGN KEY (user_id) REFERENCES user (id)
                )
            ''')

            conn.execute('''
                CREATE TABLE IF NOT EXISTS user(
                    user_id TEXT PRIMARY KEY,
                    display_name TEXT,
                    username TEXT,
                    color TEXT,
                    turbo INTEGER DEFAULT 0,
                    added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            conn.execute('''
                CREATE TABLE IF NOT EXISTS user_in_room (
                    room_id TEXT,
                    user_id TEXT,
                    last_seen TIMESTAMP,
                    returning_chatter INTEGER DEFAULT 0,
                    first_message INTEGER DEFAULT 0,
                    sub INTEGER DEFAULT 0,
                    vip INTEGER DEFAULT 0,
                    mod INTEGER DEFAULT 0,
                    badges TEXT,
                    user_type TEXT,
                    PRIMARY KEY (room_id, user_id),
                    FOREIGN KEY (room_id) REFERENCES room (id),
                    FOREIGN KEY (user_id) REFERENCES user (id)
                )
            ''')

            conn.execute('''
                CREATE TABLE IF NOT EXISTS userlist (
                    room_name TEXT,
                    display_name TEXT,
                    join_part TEXT,
                    timestamp TIMESTAMP)
            ''')

            conn.execute('CREATE INDEX IF NOT EXISTS idx_message_room_time ON message_in_room (room_id, timestamp)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_message_user ON message_in_room (user_id)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_user_in_room_last_seen ON user_in_room (room_id, last_seen)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_subs_room_time ON subs (room_id, timestamp)')

    def execute_query(self, query:str, params:tuple=()):
        """Execute a query against the database"""

        pass

    def execute_query_all(self, query:str, params:tuple=()) -> Optional[List[tuple]]:
        """Execute a query and return all results"""

        pass