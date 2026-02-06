from dataclasses import dataclass
from .baseTag import BaseTag

@dataclass
class PaidupgradeTag(BaseTag):

    # giftpaidupgrade
    msg_param_sender_login:str | None = None
    msg_param_sender_name:str | None = None
    
    # primepaidupgrade 
    msg_param_sub_plan:str | None = None

    # general
    system_msg:str | None = None