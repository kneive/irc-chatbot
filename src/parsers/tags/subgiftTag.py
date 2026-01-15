from .baseTag import BaseTag
from dataclasses import dataclass

@dataclass
class SubgiftTag(BaseTag):

    sub:str = ''
    vip:str = ''
    mod:str = ''

    gift_id:str = ''
    origin_id:str = ''
    gift_months:str = ''
    months:str = ''

    recipient_id:str = ''
    recipient_display_name:str = ''
    recipient_username:str = ''

    sender_count:str = ''
    sub_plan:str = ''
    sub_plan_name:str = ''

    msg_id:str = ''
    source_msg_id:str = ''
    
    

