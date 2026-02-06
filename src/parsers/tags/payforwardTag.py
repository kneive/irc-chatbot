from dataclasses import dataclass
from .baseTag import BaseTag

@dataclass
class PayforwardTag(BaseTag):

    # communitypayforward + standardpayforward
    msg_param_prior_gifter_anonymous:str
    msg_param_prior_gifter_display_name:str
    msg_param_prior_gifter_id:str
    msg_param_prior_gifter_user_name:str

    # standardpayforward
    msg_param_recipient_display_name:str
    msg_param_recipient_id:str
    msg_param_recipient_user_name:str

    # general

    system_msg:str