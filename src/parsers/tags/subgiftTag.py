from .baseTag import BaseTag
from dataclasses import dataclass

@dataclass
class SubgiftTag(BaseTag):

    sub:str = 'null'
    vip:str = 'null'
    mod:str = 'null'

    gift_id:str = 'null'
    origin_id:str = 'null'
    gift_months:str = 'null'
    months:str = 'null'

    recipient_id:str = 'null'
    recipient_display_name:str = 'null'
    recipient_username:str = 'null'

    sender_count:str = 'null'
    sub_plan:str = 'null'
    sub_plan_name:str = 'null'

    #msg_id:str = 'null'
    #source_msg_id:str = 'null'
    
    

