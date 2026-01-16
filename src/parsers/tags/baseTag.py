from dataclasses import dataclass

@dataclass
class BaseTag:
    user_id:str = 'null'
    display_name:str = 'null' 
    username:str = 'null'

    badge_info:str = 'null'
    badges:str = 'null'
    source_badge_info:str = 'null'
    source_badges:str = 'null'

    turbo:str = 'null'
    returning_chatter:str = 'null'
    first_msg:str = 'null'

    color:str = 'null'
    emotes:str = 'null'
    flags:str = 'null'
    user_type:str = 'null'

    room_id:str = 'null'
    source_room_id:str = 'null'
    room_name:str = 'null'

    id:str = 'null'
    msg_id:str = 'null'
    source_msg_id:str = 'null'
    tmi_sent_ts:str = 'null'