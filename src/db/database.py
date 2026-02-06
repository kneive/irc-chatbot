import sqlite3
from typing import List, Optional

class DatabaseManager:
    def __init__(self, db_path='saltmine.db'):
        self.db_path = db_path
        self.setup_database()

    def setup_database(self):
        """Create all tables"""
        with sqlite3.connect(self.db_path) as conn:

            # maybe redesign?
            conn.execute('''
                CREATE TABLE IF NOT EXISTS announcement (
                    serial INTEGER PRIMARY KEY AUTOINCREMENT,
                    room_id TEXT REFERENCES room (room_id),
                    user_id TEXT REFERENCES user (user_id),
                    display_name TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    msg_content TEXT
                )             
            ''')

            conn.execute('''
                CREATE TABLE IF NOT EXISTS bits (
                    serial INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT REFERENCES user (user_id),
                    room_id TEXT REFERENCES room (room_id),
                    source_room_id TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    bits INTEGER
                )
            ''')

            conn.execute('''
                CREATE TABLE IF NOT EXISTS bitsbadgetier (
                    serial INTEGER PRIMARY KEY AUTOINCREMENT,
                    room_id TEXT REFERENCES room (room_id),
                    user_id TEXT REFERENCES user (user_id),
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    msg_param_threshold INTEGER DEFAULT 0,
                    system_msg TEXT
                )          
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS user (
                    user_id TEXT PRIMARY KEY,
                    login TEXT DEFAULT '',
                    display_name TEXT DEFAULT '',
                    user_type TEXT DEFAULT '',
                    turbo INTEGER DEFAULT 0,
                    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            conn.execute('''
                CREATE TABLE IF NOT EXISTS room (
                    room_id TEXT PRIMARY KEY,
                    room_name TEXT DEFAULT '#UNKNOWN',
                    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            conn.execute('''
                CREATE TABLE IF NOT EXISTS user_in_room (
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP PRIMARY KEY,
                    user_id TEXT REFERENCES user (user_id),
                    room_id TEXT REFERENCES room (room_id),
                    badges TEXT DEFAULT '',
                    badge_info TEXT DEFAULT '',
                    subscriber INTEGER DEFAULT 0,
                    sub_streak INTEGER DEFAULT 0,
                    vip INTEGER DEFAULT 0,
                    mod INTEGER DEFAULT 0
                )
            ''')

            conn.execute('''
                CREATE TABLE IF NOT EXISTS privmsg (
                    serial INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    tmi_sent_ts TEXT NOT NULL,
                    message_id TEXT NOT NULL,
                    source_message_id TEXT,
                    room_id TEXT REFERENCES room (room_id),
                    source_room_id TEXT DEFAULT 'NULL',
                    user_id TEXT REFERENCES user (user_id),
                    color TEXT DEFAULT '',
                    returning_chatter INTEGER DEFAULT 0,
                    first_msg INTEGER DEFAULT 0,
                    flags TEXT DEFAULT '',
                    emotes TEXT DEFAULT '',
                    msg_content TEXT DEFAULT '',
                    reply_user_id TEXT REFERENCES user (user_id),
                    reply_msg_id TEXT,
                    reply_msg_body TEXT,
                    thread_user_id TEXT REFERENCES user (user_id),
                    thread_msg_id TEXT
                )
            ''')

            conn.execute('''
                CREATE TABLE IF NOT EXISTS raid (
                    serial INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT REFERENCES user (user_id),
                    room_id TEXT REFERENCES room (room_id),
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    tmi_sent_ts TEXT NOT NULL,
                    msg_id TEXT NOT NULL,
                    source_msg_id TEXT,
                    msg_param_displayName TEXT,
                    msg_param_login TEXT,
                    msg_param_profileImageURL TEXT,
                    msg_param_viewerCount TEXT,
                    system_msg TEXT NOT NULL
                )
            ''')

            conn.execute('''
                CREATE TABLE IF NOT EXISTS sub(
                    serial INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT REFERENCES user (user_id),
                    room_id TEXT REFERENCES room (room_id),
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    tmi_sent_ts TEXT NOT NULL,
                    msg_id TEXT NOT NULL,
                    source_msg_id TEXT,
                    cumulative_months INTEGER DEFAULT 0,
                    months INTEGER DEFAULT 0,
                    multimonth_duration INTEGER DEFAULT 0,
                    multimonth_tenure INTEGER DEFAULT 0,
                    should_share_streak INTEGER DEFAULT 0,
                    sub_plan_name TEXT,
                    sub_plan TEXT NOT NULL,
                    was_gifted TEXT NOT NULL,
                    system_msg TEXT
                )            
            ''')

            conn.execute('''
                CREATE TABLE IF NOT EXISTS subgift(
                    serial INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT REFERENCES user (user_id),
                    room_id TEXT REFERENCES room (room_id),
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    tmi_sent_ts TEXT NOT NULL,
                    msg_id TEXT NOT NULL,
                    source_msg_id TEXT,
                    community_gift_id TEXT,
                    fun_string TEXT,
                    gift_months INTEGER DEFAULT 0,
                    months INTEGER DEFAULT 0,
                    origin_id TEXT,
                    recipient_id TEXT,
                    recipient_display_name TEXT,
                    recipient_user_name TEXT,
                    sender_count INTEGER DEFAULT 0,
                    sub_plan_name TEXT,
                    sub_plan TEXT,
                    system_msg TEXT
                )
            ''')

            conn.execute('''
                CREATE TABLE IF NOT EXISTS submysterygift (
                    serial INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT REFERENCES user (user_id),
                    room_id TEXT REFERENCES room (room_id),
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    tmi_sent_ts TEXT NOT NULL,
                    msg_id TEXT NOT NULL,
                    source_msg_id TEXT,
                    community_gift_id TEXT NOT NULL,
                    contribution_type TEXT,
                    current_contributions INTEGER DEFAULT 0,
                    target_contributions INTEGER DEFAULT 0,
                    user_contributions INTEGER DEFAULT 0,
                    mass_gift_count INTEGER DEFAULT 0,
                    origin_id TEXT,
                    sub_plan TEXT,
                    system_msg TEXT NOT NULL
                )
            ''')

            conn.execute('''
                CREATE TABLE IF NOT EXISTS payforward (
                    serial INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT REFERENCES user (user_id),
                    room_id TEXT REFERENCES room (room_id),
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    tmi_sent_ts TEXT NOT NULL,
                    msg_id TEXT NOT NULL,
                    source_msg_id TEXT,
                    prior_gifter_anonymous TEXT,
                    prior_gifter_id TEXT REFERENCES user (user_id),
                    prior_gifter_display_name TEXT,
                    prior_gifter_user_name TEXT,
                    recipient_id TEXT,
                    recipient_display_name TEXT,
                    recipient_user_name TEXT,
                    system_msg TEXT NOT NULL
                )
            ''')

            conn.execute('''
                CREATE TABLE IF NOT EXISTS paidupgrade (
                    serial INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT REFERENCES user (user_id),
                    room_id TEXT REFERENCES room (room_id),
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    tmi_sent_ts TEXT NOT NULL,
                    msg_id TEXT NOT NULL,
                    source_msg_id TEXT,
                    sender_login TEXT,
                    sender_name TEXT,
                    sub_plan TEXT,
                    system_msg TEXT NOT NULL
                )
            ''')

            conn.execute('''
                CREATE TABLE IF NOT EXISTS onetapgift (
                    serial INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT REFERENCES user (user_id),
                    room_id TEXT REFERENCES room (room_id),
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    tmi_sent_ts TEXT NOT NULL,
                    msg_id TEXT NOT NULL,
                    source_msg_id TEXT,
                    bits_spent INTEGER DEFAULT 0,
                    gift_id TEXT NOT NULL,
                    user_display_name TEXT,
                    system_msg TEXT NOT NULL
                )
            ''')

            conn.execute('''
                CREATE TABLE IF NOT EXISTS roomstate (
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    room_id TEXT PRIMARY KEY,
                    emote_only INTEGER DEFAULT 0,
                    followers_only INTEGER DEFAULT 0,
                    r9k INTEGER DEFAULT 0,
                    slow INTEGER DEFAULT 0,
                    subs_only INTEGER DEFAULT 0
                )
            ''')

            conn.execute('''
                CREATE TABLE IF NOT EXISTS userlist (
                    serial INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    room_name TEXT NOT NULL,
                    room_id TEXT,
                    username TEXT NOT NULL,
                    join_part TEXT NOT NULL
                )
            ''')

            # maybe redesign?
            conn.execute('''
                CREATE TABLE IF NOT EXISTS viewermilestone(
                    serial INTEGER PRIMARY KEY AUTOINCREMENT,
                    room_id TEXT REFERENCES room (room_id),
                    user_id TEXT REFERENCES user (user_id),
                    display_name TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    streak INTEGER DEFAULT 0,
                    system_msg TEXT
                )
            ''')


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