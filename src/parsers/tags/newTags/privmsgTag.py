from dataclasses import dataclass
from .baseTag import BaseTag

@dataclass
class PrivmsgTag(BaseTag):
    
    first_msg:int
    returning_chatter:int
    turbo:int
    msg_content:str