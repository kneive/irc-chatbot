from dataclasses import dataclass

@dataclass
class RoomstateTag:
    room_id:str = 'null'

    emote_only:str = '-1'
    followers_only:str = '-1'
    r9k:str = '-1'
    slow_mode:str = '-1'
    sub_only:str = '-1'