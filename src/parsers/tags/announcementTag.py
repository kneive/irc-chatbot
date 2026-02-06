from .baseTag import BaseTag
from dataclasses import dataclass

@dataclass
class AnnouncementTag(BaseTag):
    
    param_color:str | None = None
    system_msg:str | None = None
    msg_content:str | None = None