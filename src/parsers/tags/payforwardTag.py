from dataclasses import dataclass
from .baseTag import BaseTag

@dataclass
class PayforwardTag(BaseTag):

    # communitypayforward + standardpayforward
    msg_param_prior_gifter_anonymous:str | None = None
    msg_param_prior_gifter_display_name:str | None = None
    msg_param_prior_gifter_id:str | None = None
    msg_param_prior_gifter_user_name:str | None = None

    # standardpayforward
    msg_param_recipient_display_name:str | None = None
    msg_param_recipient_id:str | None = None
    msg_param_recipient_user_name:str | None = None

    # general

    system_msg:str | None = None