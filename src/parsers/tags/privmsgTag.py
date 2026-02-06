from dataclasses import dataclass
from .baseTag import BaseTag

@dataclass
class PrivmsgTag(BaseTag):
    
    message_id:str | None = None
    source_message_id:str | None = None
    first_msg:int=-42
    returning_chatter:int=-42
    msg_content:str | None = None

    #add reply and thread