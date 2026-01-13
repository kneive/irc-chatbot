class Saltminer:

    def _check_user(self, user_id:str) -> bool:
        """Check wheter user table contains user_id"""

        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                SELECT 1 FROM user WHERE id = ?
            ''', (user_id,))

        return conn.fetchone() is not None

    def _check_room(self, room_id:str) -> bool:
            """Check whether room table contains room_id"""

            with sqlite3.connect(self.db_path) as conn:
                conn.execute('''
                    SELECT 1 FROM room WHERE id = ?
                ''', (room_id,))

            return conn.fetchone() is not None

    def _check_user_in_room(self, room_id:str, user_id:str) -> bool:
        """Check whether the user has been seen in the room before"""

        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                SELECT 1 FROM user_in_room WHERE room_id = ? AND user_id = ?
            ''', (room_id, user_id))

            return conn.fetchone() is not None

    def upsert_room(self, room_id:str, room_name:str) -> None:
        """Insert or update room table"""

        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT OR REPLACE INTO room (id, name) VALUES (?, ?)
            ''', (room_id, room_name))


    def upsert_user(self, 
                    user_id:str, 
                    display_name:str, 
                    username:str, 
                    color:str=None, 
                    turbo:int=0) -> None:
        """Insert or update user table"""

        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT OR REPLACE INTO user 
                (id, display_name, username, color, turbo)
                VALUES (?,?,?,?,?)
            ''', (user_id, display_name, username, color, turbo))

    def upsert_user_in_room(self, 
                            room_id:str, 
                            user_id:str,
                            returning_chatter:int=0,
                            first_message:int=0,
                            sub:int=0,
                            vip:int=0,
                            mod:int=0,
                            badges:str='',
                            user_type:str='') -> None:
        """Insert or update user_in_room table"""

        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT OR REPLACE INTO user_in_room
                (room_id, user_id, last_seen, returning_chatter, first_message, 
                 sub, vip, mod, badges, user_type)
                VALUES (?,?,CURRENT_TIMESTAMP,?,?,?,?,?,?,?)
            ''', (room_id, user_id, returning_chatter, first_message, sub, vip, 
                  mod, badges, user_type))

    def upsert_roomstate(self,
                         room_id:str,
                         follow_only:int=0,
                         sub_only:int=0,
                         emote_only:int=0,
                         slow_mode:int=0,
                         r9k:int=0) -> None:
        """Insert or update roomstate table"""

        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT OR REPLACE INTO roomstate
                (room_id, timestamp,follow_only, sub_only, emote_only, slow_mode, r9k)
                VALUES (?,CURRENT_TIMESTAMP,?,?,?,?,?)
            ''', (room_id, follow_only, sub_only, emote_only, slow_mode, r9k))

    def insert_message_in_room(self,
                               message_id:str,
                               room_id:str,
                               user_id:str,
                               reply_message_id:str,
                               reply_user_id:str,
                               reply_display_name:str,
                               thread_message_id:str,
                               thread_user_id:str,
                               thread_display_name:str) -> None:
        """Insert into message_in_room"""

        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT INTO message_in_room
                (message_id, room_id, user_id, timestamp, reply_message_id, 
                reply_user_id, reply_display_name, thread_message_id, 
                thread_user_id, thread_display_name)
                VALUES (?,?,?,CURRENT_TIMESTAMP,?,?,?,?,?,?)
            ''', (message_id, room_id, user_id, reply_message_id, reply_user_id, 
                  reply_display_name, thread_message_id, thread_user_id, 
                  thread_display_name))

    def insert_subs(self,
                    user_id:str,
                    room_id:str,
                    message_id:str,
                    gift_id:str,
                    sub_plan:str,
                    months:int=0,
                    gift_months:int=0,
                    multimonth_duration:int=0,
                    multimonth_tenure:int=0,
                    streak_months:int=0,
                    share_streak:int=0,
                    cumulative:int=0) -> None:
        """Insert into subs table"""

        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT INTO subs
                (user_id, room_id, timestamp, message_id, gift_id, sub_plan, 
                months, gift_months, multimonth_duration, multimonth_tenure, 
                streak_months, share_streak, cumulative)
                VALUES (?,?,CURRENT_TIMESTAMP,?,?,?,?,?,?,?,?,?,?)
            ''', (user_id, room_id, message_id, gift_id, sub_plan, months, 
                  gift_months, multimonth_duration, multimonth_tenure, 
                  streak_months, share_streak, cumulative))
        
    def insert_subgift(self,
                        user_id:str,
                        room_id:str,
                        gift_id:str,
                        gift_count:int=0,
                        gifter_total:int=0,
                        sub_plan:str=None) -> None:
        """Insert into subgift table"""

        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT INTO subgift
                (user_id, room_id, timestamp, gift_id, 
                    gift_count, gifter_total, sub_plan)
                VALUES (?,?,CURRENT_TIMESTAMP,?,?,?,?)
            ''', (user_id, room_id, gift_id, gift_count, 
                  gifter_total, sub_plan))
            
    def insert_bits(self,
                    user_id:str,
                    room_id:str,
                    source_room_id:str,
                    bits:int) -> None:
        """Insert into bits table"""

        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT INTO bits
                (user_id, room_id, timestamp, source_room_id, bits)
                VALUES (?,?,CURRENT_TIMESTAMP,?,?)
            ''', (user_id, room_id, source_room_id, bits))
    
    def insert_raid(self,
                    room_id,
                    user_id,
                    source_room_id,
                    viewer_count) -> None:
        """Insert into raid table"""

        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT INTO raid
                (room_id, user_id, timestamp, source_room_id, viewer_count)
                VALUES (?,?,CURRENT_TIMESTAMP,?,?)
            ''', (room_id, user_id, source_room_id, viewer_count))

    def insert_userlist(self,
                        room_name:str,
                        display_name:str,
                        join_part:str) -> None:
        """Insert into userlist table"""

        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT INTO userlist
                (room_name, display_name, join_part, timestamp)
                VALUES (?,?,?,CURRENT_TIMESTAMP)
            ''', (room_name, display_name, join_part))

    def get_user(self, user_id:str) -> Optional[User]:
        """Get entry for a single user from user table"""

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('''
                        SELECT user_id, display_name, username, color, turbo
                        FROM user
                        WHERE user_id = ?
                    ''', (user_id))
            
            entry = cursor.fetchone()

            if entry:
                return User(user_id=entry[0],
                            display_name=entry[1],
                            username=entry[2],
                            color=entry[3],
                            turbo=entry[4])
            
            return None
        
    def get_roomstate(self, room_id:str) -> Optional[Roomstate]:
        """Get entry for a single room from roomstate table"""

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('''
                        SELECT room_id, timestamp, follow_only, sub_only, 
                               emote_only, slow_mode, r9k
                        FROM roomstate
                        WHERE room_id = ?
                    ''')
            entry = cursor.fetchone()
            if entry:
                return Roomstate(room_id=entry[0],
                                 timestamp=datetime.fromisoformat(entry[1]),
                                 follow_only=entry[2],
                                 sub_only=entry[3],
                                 emote_only=entry[4],
                                 slow_mode=entry[5],
                                 r9k=entry[6])
            
            return None