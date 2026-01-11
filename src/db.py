import sqlite3
import json
from datetime import datetime
from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass

@dataclass
class Room:
    room_id:str | None = None
    name:str='unknown'

@dataclass
class User:
    user_id: str | None = None
    display_name: str | None = None
    username: str | None = None
    color: str | None = None
    turbo: int = 0 

@dataclass
class Roomstate:
    room_id: str | None = None
    timestamp: datetime | None = None
    follow_only: int = 0
    sub_only: int = 0
    emote_only: int = 0
    slow_mode: int = 0
    r9k: int = 0

@dataclass
class UserInRoom:
    room_id:str | None = None
    user_id:str | None = None
    returning_chatter:int=0
    first_message:int=0
    sub:int=0
    vip:int=0
    mod:int=0
    badges:str=''
    user_type:str=''


@dataclass
class MessageInRoom:
    message_id:str | None = None
    room_id:str | None = None
    user_id:str | None = None
    reply_message_id:str=''
    reply_user_id:str=''
    reply_display_name:str=''
    thread_message_id:str=''
    thread_user_id:str=''
    thread_display_name:str=''

@dataclass
class Sub:
    user_id:str | None = None
    room_id:str | None = None
    message_id:str | None = None
    gift_id:str=''
    sub_plan:str | None = None
    months:int=0
    gift_monts:int=0
    multimonth_duration:int=0
    multimonth_tenure:int=0
    streak_months:int=0
    share_streak:int=0
    cumulative:int=0

@dataclass
class Subgift:
    user_id:str | None = None
    room_id:str | None = None
    source_room_id:str | None = None
    gift_id:str | None = None
    gift_count:int=0
    gifter_total:int=0
    sub_plan:str | None = None


class TwitchChadDB:
    def __init__(self, db_path='twitch_chat.db'):
        self.db_path = db_path
        self.setup_database()

    def setup_database(self):
        """Create all tables for the database"""
        with sqlite3.connect(self.db_path) as conn:

            conn.execute('''
                CREATE TABLE IF NOT EXISTS room (
                    room_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL
                )             
            ''')

            conn.execute('''
                CREATE TABLE IF NOT EXISTS user(
                    user_id TEXT PRIMARY KEY,
                    display_name TEXT,
                    username TEXT,
                    color TEXT,
                    turbo INTEGER DEFAULT 0
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
                return User(
                    user_id=entry[0],
                    display_name=entry[1],
                    username=entry[2],
                    color=entry[3],
                    turbo=entry[4]
                )
            
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
                return Roomstate(
                    room_id=entry[0],
                    timestamp=datetime.fromisoformat(entry[1]),
                    follow_only=entry[2],
                    sub_only=entry[3],
                    emote_only=entry[4],
                    slow_mode=entry[5],
                    r9k=entry[6]
                )
            
            return None

##### baustelle

    def parse_privmsg(self, message:str) -> None:
        """Parse tags into dictionary"""

        try:
            # we build a separator ' :{display-name}' to separate tags and message
            start = message.find('display-name=')
            if start == -1:
                raise ValueError("PRIVMSG message is corrupted: no 'display-name'")
            
            start +=  len('display-name=')
            end = message.find(';', start)
            if end == -1:
                raise ValueError("PRIVMSG message is corrupted: no ';' after display-name")
            
            separator = f' :{message[start:end]}'

            # find the end of tags
            boundary = message.find(separator)
            if boundary == -1:
                raise ValueError("PRIVMSG message is corrupted: cannot separate tags from message part")

            parsed = {}
            tags = message[1:boundary]
            for tag in tags.split(';'):
                if '=' in tag:
                    key, value = tag.split('=', 1)
                    parsed[key] = value if value else None
            
            # parse message
            message = message[boundary+2:]  # skip first ' :'
            
            idx = message.find('#')
            if idx == -1:
                raise ValueError("PRIVMSG message is corrupted: no '#' in message part")
            room_name = message[idx+1:message.find(' ', idx)].strip()

            idx = message.find(' :')
            if idx == -1:
                raise ValueError("PRIVMSG message is corrupted: no ' :' in message part")

            # add to message in channel table

            # check whether user is present in user table
            if not self._check_user(parsed.get('user-id')):
                self.upsert_user(user_id=parsed.get('user-id'),
                                 display_name=parsed.get('display-name'),
                                 username=parsed.get('display-name').lower(),
                                 color=parsed.get('color'),
                                 turbo=int(parsed.get('turbo', '0')))
            
            # check whether room/source-room is present in room table             
            if ('source-room-id' in parsed and 
                not self._check_room(parsed.get('source-room-id'))):
                
                self.upsert_room(room_id=parsed.get('source-room-id'),
                                 room_name='unknown')
                
            if not self._check_room(parsed.get('room-id')):

                self.upsert_room(room_id=parsed.get('room-id'),
                                room_name=room_name)

            # upsert user in user_in_room table
            user_room = UserInRoom(user_id=parsed.get('user-id'),
                                   returning_chatter=int(parsed.get('returning-chatter')),
                                   first_message=int(parsed.get('first-message')),
                                   sub=int(parsed.get('subscriber')),
                                   badges=parsed.get('badges'),
                                   user_type=parsed.get('user-type'))
            
            if 'source-room-id' in parsed:
                user_room.room_id=parsed.get('source-room-id')
            else:
                user_room.room_id=parsed.get('room-id')

            if self._check_user_in_room(room_id=user_room.room_id):

                if parsed.get('source-badge') is 'vip':
                    user_room.vip=1
                elif parsed.get('mod') is '1':
                    user_room.mod=1
                            
                self.upsert_user_in_room(room_id=user_room.room_id,
                                        user_id=user_room.user_id,
                                        returning_chatter=user_room.returning_chatter,
                                        first_message=user_room.first_message,
                                        sub=user_room.sub,
                                        vip=user_room.vip,
                                        mod=user_room.mod,
                                        badges=user_room.badges,
                                        user_type=user_room.user_type)

            # add message to message_in_room
            message = MessageInRoom(message_id=parsed.get('id'),
                                    user_id=parsed.get('user-id'))
            if 'source-room-id' in parsed:
                message(room_id=parsed.get('source-room-id'))
            else:
                message(room_id=parsed.get('room-id'))
            if 'reply-parent-msg-id' in parsed:
                message(reply_message_id=parsed.get('reply-parent-msg-id'))
                message(reply_user_id=parsed.get('reply-parent-user-id'))
                message(reply_display_name=parsed.get('reply-parent-display-name'))
            if 'reply-thread-parent-msg-id' in parsed:
                message(thread_message_id=parsed.get('reply-thread-parent-msg-id'))
                message(thread_user_id=parsed.get('reply-thread-parent-user-id'))
                message(thread_display_name=parsed.get('reply-thread-parent-display-name'))

            self.insert_message_in_room(message.message_id,
                                        message.user_id,
                                        message.room_id,
                                        message.reply_message_id,
                                        message.reply_user_id,
                                        message.reply_display_name,
                                        message.thread_message_id,
                                        message.thread_user_id,
                                        message.thread_display_name)

        except Exception as e:
            print(f'Error parsing PRIVMSG: {e}')

    def parse_usernotice(self, message:str) -> None:
        """Parse USERNOTICE messages"""

        try:
            tags_end = message.find(' :tmi.twitch.tv')
            if tags_end == -1:
                raise ValueError("USERNOTICE message is corrupted: no ' :'")

            idx = message[tags_end:].find(' #')
            if idx == -1:
                raise ValueError("USERNOTICE message is corrupted: no '#'")
            
            room_name = message[idx+1:].strip()
            tags = message[1:tags_end]
            tags_parsed = {}
            for tag in tags.split(';'):
                if '=' in tag:
                    key, value = tag.split('=',1)
                    tags_parsed[key] = value if value else None
            
            if tags_parsed == {}:
                raise ValueError("USERNOTICE message is corrupted: no tags")
            
            # check whether user is present in user table
            if not self._check_user(tags_parsed.get('user-id')):
                self.upsert_user(user_id=tags_parsed.get('user-id'),
                                    display_name=tags_parsed.get('display-name'),
                                    username=tags_parsed.get('display-name').lower(),
                                    color=tags_parsed.get('color'),
                                    turbo=int(tags_parsed.get('turbo', '0')))

            # check whether room is present
            if ('msg-id' == 'sharedchatnotice' and 
                not self._check_room(tags_parsed.get('source-room-id'))):
            
                self.upsert_room(room_id=tags_parsed.get('source-room-id'),
                                room_name='unknown')
            
            if not self._check_room(tags_parsed.get('room-id')):

                self.upsert_room(room_id=tags_parsed.get('room-id'),
                                room_name=room_name)

            # upsert user in user_in_room table
            user_room = UserInRoom(user_id=tags_parsed.get('user-id'),
                                sub=int(tags_parsed.get('subscriber')),
                                badges=tags_parsed.get('badges'),
                                user_type=tags_parsed.get('user-type'))
            
            if 'msg-id' == 'sharedchatnotice':
                user_room.room_id=tags_parsed.get('source-room-id')
            else:
                user_room.room_id=tags_parsed.get('room-id')

            if self._check_user_in_room(room_id=user_room.room_id):

                if tags_parsed.get('vip') is '1':
                    user_room.vip=1
                elif tags_parsed.get('mod') is '1':
                    user_room.mod=1
                            
                self.upsert_user_in_room(room_id=user_room.room_id,
                                        user_id=user_room.user_id,
                                        returning_chatter=user_room.returning_chatter,
                                        first_message=user_room.first_message,
                                        sub=user_room.sub,
                                        vip=user_room.vip,
                                        mod=user_room.mod,
                                        badges=user_room.badges,
                                        user_type=user_room.user_type)

            # sub, resub
            if (tags_parsed.get('msg-id') in ['sub', 'resub'] or 
                tags_parsed.get('source-msg-id') in ['sub', 'resub']):
            
                # sub, resub
                sub = Sub(user_id=tags_parsed.get('user-id'),
                        sub_plan=tags_parsed.get('msg-param-sub-plan'),
                        months=int(tags_parsed.get('msg-param-months')),
                        multimonth_duration=int(tags_parsed.get('msg-param-multimonth-duration')),
                        multimonth_tenure=int(tags_parsed.get('msg-param-multimonth-tenure')),
                        streak_months=0,
                        share_streak=int(tags_parsed.get('msg-param-should-share-streak')),
                        cumulative=int(tags_parsed.get('msg-param-cumulative-months')))
                if tags_parsed.get('msg-id') == 'sharedchatnotice':
                    sub.room_id=tags_parsed.get('source-room-id')
                    sub.message_id=tags_parsed.get('source-id')
                else:
                    sub.room_id=tags_parsed.get('room-id')
                    sub.message_id=tags_parsed.get('id')

                #if tags_parsed.get('msg-param-was-gifted') == 'true':
                #    Sub.gift_id=tags_parsed.get('???')
                #    Sub.gift_months=int(tags_parsed.get('???'))
                
                #placeholder for gift_id and gift_months
                sub.gift_id=''
                sub.gift_months=0

                self.insert_subs(user_id=sub.user_id,
                                 room_id=sub.room_id,
                                 message_id=sub.message_id,
                                 gift_id=sub.gift_id,
                                 sub_plan=sub.sub_plan,
                                 months=sub.months,
                                 gift_months=sub.gift_months,
                                 multimonth_duration=sub.multimonth_duration,
                                 multimonth_tenure=sub.multimonth_tenure,
                                 streak_months=sub.streak_months,
                                 share_streak=sub.share_streak,
                                 cumulative=sub.cumulative)

            # subgift, submysterygift 
            if (tags_parsed.get('msg-id') in ['subgift', 'submysterygift'] or 
                tags_parsed.get('source-msg-id') in ['subgift', 'submysterygift']):
            
                if (tags_parsed.get('msg-id') == 'subgift' or 
                    tags_parsed.get('source-msg-id') == 'subgift'):
                
                    gift = Subgift(user_id=tags_parsed.get('user-id'),
                                   gift_id=tags_parsed.get('msg-param-community-gif-id'),
                                   gift_count=0,
                                   gifter_total=tags_parsed.get('msg-param-sender-count'),
                                   sub_plan=tags_parsed.get('msg-param-sub-plan'))

                    sub = Sub(user_id=tags_parsed.get('msg-param-recipient-id'),
                              room_id=gift.room_id,
                              gift_id=tags_parsed.get('msg-param-community-gift-id'),
                              sub_plan=tags_parsed.get('msg-param-sub-plan'),
                              months=tags_parsed.get('msg-param-months'),
                              gift_months=tags_parsed.get('msg-param-gift-months'),
                              multimonth_duration=0,
                              multimonth_tenure=0,
                              streak_months=0,
                              share_streak=0,
                              cumulative=0)

                    if tags_parsed.get('msg-id') == 'sharedchatnotice':
                        gift.room_id=tags_parsed.get('sourceroom-id')
                        sub.message_id=tags_parsed.get('source-id')
                    else:
                        gift.room_id=tags_parsed.get('room-id')
                        sub.message_id=tags_parsed.get('id')

                    self.insert_subgift(user_id=gift.user_id,
                                        room_id=gift.room_id,
                                        gift_id=gift.gift_id,
                                        gift_count=gift.gift_count,
                                        gifter_total=gift.gifter_total,
                                        sub_plan=gift.sub_plan)
                    
                    self.insert_subs(user_id=sub.user_id,
                                 room_id=sub.room_id,
                                 message_id=sub.message_id,
                                 gift_id=sub.gift_id,
                                 sub_plan=sub.sub_plan,
                                 months=sub.months,
                                 gift_months=sub.gift_months,
                                 multimonth_duration=sub.multimonth_duration,
                                 multimonth_tenure=sub.multimonth_tenure,
                                 streak_months=sub.streak_months,
                                 share_streak=sub.share_streak,
                                 cumulative=sub.cumulative)
                
                else:
                    gift = Subgift(user_id=tags_parsed.get('user-id'),
                                   gift_id=tags_parsed.get('msg-param-community-gif-id'),
                                   gift_count=int(tags_parsed.get('msg-param-mass-gift-count')),
                                   gifter_total=int(tags_parsed.get('msg-param-sender-count')),
                                   sub_plan=tags_parsed.get('msg-param-sub-plan'))

                    if tags_parsed.get('msg-id') == 'sharedchatnotice':
                        gift.room_id=tags_parsed.get('source-room-id')
                    else:
                        gift.room_id=tags_parsed.get('room-id')

                    self.insert_subgift(user_id=gift.user_id,
                                        room_id=gift.room_id,
                                        gift_id=gift.gift_id,
                                        gift_count=gift.gift_count,
                                        gifter_total=gift.gifter_total,
                                        sub_plan=gift.sub_plan)
     
            # watch-streak - not implemented yet
                
        except Exception as e:
            print(f'Error parsing USERNOTICE: {e}')
        
    def parse_join(self, message:str) -> None:
        """Parse channel JOIN message"""

        try:
            idx = message.find('!')
            if idx == -1:
                raise ValueError("JOIN message is corrupted: no '!'")

            display_name = message[1:idx]

            idx = message.find('JOIN #')
            if idx == -1:
                raise ValueError("JOIN messaee is corrupted: no '#'")

            room_name = message[idx+1:].strip()

            # Add upsert into userlist
            self.insert_userlist(room_name=room_name,
                                 display_name=display_name,
                                 join_part='JOIN')

        except Exception as e:
            print(f'Error parsing JOIN: {e}')


    def parse_part(self, message:str) -> None:
        """Parse channel PART message"""

        try:
            idx = message.find('!')
            if idx == -1:
                raise ValueError("PART message is corrupted: no '!'")
            
            display_name = message[1:idx]

            idx = message.find('PART #')
            if idx == -1:
                raise ValueError("PART message is corrupted: no '#'")
            
            room_name = message[idx+1:].strip()

            # Add upsert into userlist

            self.insert_userlist(room_name=room_name,
                                 display_name=display_name,
                                 join_part='PART')

        except Exception as e:
            print(f'Error parsing PART: {e}')

    def parse(self, line:str) -> None:
        """Parse IRC line into dictionary"""

        if ' PRIVMSG ' in line:
            self.parse_privmsg(line)

        if ' USERNOTICE ' in line:
            self.parse_usernotice(line)

        if ' JOIN ' in line:
            self.parse_join(line)
    
        if ' PART ' in line:
            self.parse_part(line)