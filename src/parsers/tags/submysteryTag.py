from .baseTag import BaseTag
from dataclasses import dataclass

@dataclass
class SubmysterygiftTag(BaseTag):

    sub:str = 'null'
    vip:str = 'null'
    mod:str = 'null'

    gift_id:str = 'null'
    origin_id:str = 'null'
    sub_plan:str = 'null'
    mass_gift_count:str = 'null'
    sender_count:str = 'null'
    
    #msg_id:str = 'null'
    #source_msg_id:str = 'null'