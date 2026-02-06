from dataclasses import dataclass
from .baseTag import BaseTag

@dataclass
class PrivmsgTag(BaseTag):
    
    message_id:str
    source_message_id:str
    first_msg:int=-42
    returning_chatter:int=-42
    turbo:int=-42
    msg_content:str

    #add reply and thread