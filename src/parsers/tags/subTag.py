from dataclasses import dataclass
from .baseTag import BaseTag

@dataclass
class SubTag(BaseTag):

    # msg params
    msg_param_cumulative_months:int=-42
    msg_param_months:int=-42
    msg_param_multimonth_duration:int=-42
    msg_param_multimonth_tenure:int=-42
    msg_param_should_share_streak:int=-42
    msg_param_sub_plan_name:str | None = None
    msg_param_sub_plan:str | None = None
    msg_param_was_gifted:str | None = None

    # general
    system_msg:str | None = None