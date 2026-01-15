from .baseTag import BaseTag
from dataclasses import dataclass

@dataclass
class SubmysterygiftTag(BaseTag):

    sub:str = ''
    vip:str = ''
    mod:str = ''

    gift_id:str = ''
    origin_id:str = ''
    sub_plan:str = ''
    mass_gift_count:str = ''
    sender_count:str = ''
    
    msg_id:str = ''
    source_msg_id:str = ''