from dataclasses import dataclass
from .baseTag import BaseTag

@dataclass
class PrivmsgTag(BaseTag):
    
    message_id:str
    source_message_id:str
    first_msg:int
    returning_chatter:int
    turbo:int
    msg_content:str

    #add reply and thread