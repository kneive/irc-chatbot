from .baseTag import BaseTag
from dataclasses import dataclass

@dataclass
class AnnouncementTag(BaseTag):
    
    param_color:str = 'null'
    system_msg:str = 'null'
    msg_content:str = 'null'