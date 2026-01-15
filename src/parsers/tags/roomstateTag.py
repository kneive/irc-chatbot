from dataclasses import dataclass

@dataclass
class RoomstateTag:
    room_name:str = ''

    emote_only:str = ''
    followers_only:str = ''
    r9k:str = ''
    room_id:str = ''
    slow:str = ''
    subs_only:str = ''