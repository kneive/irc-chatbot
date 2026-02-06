from dataclasses import dataclass
from .baseTag import BaseTag

@dataclass
class SubgiftTag(BaseTag):

    # msg params
    msg_param_community_gift_id:str | None = None
    msg_param_fun_string:str | None = None
    msg_param_gift_months:int=-42
    msg_param_months:int=-42
    msg_param_origin_id:str | None = None
    msg_param_recipient_display_name:str | None = None
    msg_param_recipient_id:str | None = None
    msg_param_recipient_user_name:str | None = None
    msg_param_sender_count:int=-42
    msg_param_sub_plan_name:str | None = None
    msg_param_sub_plan:str | None = None

    # general
    system_msg:str | None = None
