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

    color:str = 'null'
    emotes:str = 'null'
    flags:str = 'null'
    user_type:str = 'null'

    room_id:str = 'null'
    source_room_id:str = 'null'
    room_name:str = 'null'

    id:str = 'null'
    tmi_sent_ts:str = 'null'

    # utility fields (present in privmsg, sub, subgift, submysterygift, announcement, milestone)
    msg_id:str = 'null'
    source_msg_id:str = 'null'

    # from privmsg
    turbo:str = '-1'
    returning_chatter:str = '-1'
    first_msg:str = '-1'

    # from privmsg, sub, subgift, submysterygift
    sub:str = '-1'
    vip:str = '-1'
    mod:str = '-1'