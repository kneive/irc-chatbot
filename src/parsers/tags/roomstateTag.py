from dataclasses import dataclass

@dataclass
class RoomstateTag:
    room_id:str

    emote_only:int=-42
    followers_only:int=-42
    r9k:int=-42
    slow_mode:int=-42
    sub_only:int=-42