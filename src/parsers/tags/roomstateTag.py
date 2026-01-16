from dataclasses import dataclass

@dataclass
class RoomstateTag:
    room_name:str = 'null'

    emote_only:str = 'null'
    followers_only:str = 'null'
    r9k:str = 'null'
    room_id:str = 'null'
    slow_mode:str = 'null'
    sub_only:str = 'null'