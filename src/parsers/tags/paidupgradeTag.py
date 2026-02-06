from dataclasses import dataclass
from .baseTag import BaseTag

@dataclass
class PaidupgradeTag(BaseTag):

    # giftpaidupgrade
    msg_param_sender_login:str
    msg_param_sender_name:str
    
    # primepaidupgrade 
    msg_param_sub_plan:str

    # general
    system_msg:str