from .baseTag import BaseTag
from dataclasses import dataclass

@dataclass
class AnnouncementTag(BaseTag):
    
    param_color:str
    system_msg:str
    msg_content:str