from dataclasses import dataclass
from .baseTag import BaseTag

@dataclass
class SubTag(BaseTag):

    sub:str = ''
    vip:str = ''
    mod:str = ''

    months:str = ''
    cumulative_months:str = ''
    multimonth_duration:str = ''
    multimonth_tenure:str = ''
    should_share_streak:str = ''

    sub_plan_name:str = ''
    sub_plan:str = ''
    was_gifted:str = ''

    msg_id:str = ''
    source_msg_id:str = ''