from dataclasses import dataclass

@dataclass
class BaseTag:
    user_id:str = ''
    display_name:str = '' 
    username:str = ''

    badge_info:str = ''
    badges:str = ''
    source_badge_info:str = ''
    source_badges:str = ''

    color:str = ''
    emotes:str = ''
    flags:str = ''
    user_type:str = ''

    room_id:str = ''
    source_room_id:str = ''
    room_name:str = ''

    id:str = ''
    tmi_sent_ts:str = ''
