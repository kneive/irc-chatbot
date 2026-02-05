from dataclasses import dataclass

@dataclass
class BaseTag:

    # room information
    room_name:str
    room_id:str
    source_room_id:str

    # user information
    user_id:str
    display_name:str
    login:str
    
    # general user information
    badge_info:str
    source_badge_info:str
    badges:str
    source_badges:str
    color:str
    emotes:str
    flags:str
    user_type:str
    subscriber:int
    sub_streak:int=-1
    vip:int
    mod:int
    
    # message information
    msg_id:str
    source_msg_id:str
    tmi_sent_ts:int