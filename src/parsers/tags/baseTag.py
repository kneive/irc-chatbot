from dataclasses import dataclass

@dataclass
class BaseTag:

    # room information
    room_name:str | None = None
    room_id:str | None = None
    source_room_id:str | None = None

    # user information
    user_id:str | None = None
    display_name:str | None = None
    login:str | None = None
    
    # general user information
    badge_info:str | None = None
    source_badge_info:str | None = None
    badges:str | None = None
    source_badges:str | None = None
    color:str | None = None
    emotes:str | None = None
    flags:str | None = None
    user_type:str | None = None
    subscriber:int=-42
    sub_streak:int=-42
    vip:int=-42
    mod:int=-42
    turbo:int=-42
    
    # message information
    msg_id:str | None = None
    source_msg_id:str | None = None
    tmi_sent_ts:int=-42