from dataclasses import dataclass
from datetime import datetime

@dataclass
class Bits:
    user_id:str | None = None
    room_id:str | None = None
    source_room_id:str=''
    bits:int=0

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
class Raid:
    room_id:str | None = None
    user_id:str | None = None
    source_room_id:str=''
    viewer_count:int=1

@dataclass
class Room:
    room_id:str | None = None
    name:str='unknown'

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
class Sub:
    user_id:str | None = None
    room_id:str | None = None
    message_id:str | None = None
    gift_id:str=''
    sub_plan:str | None = None
    months:int=0
    gift_months:int=0
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

@dataclass
class User:
    user_id: str | None = None
    display_name: str | None = None
    username: str | None = None
    color: str | None = None
    turbo: int = 0 

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
class UserListEntry:
    room_name:str | None = None
    display_name:str | None = None
    join_part:str | None = None