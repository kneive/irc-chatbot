from dataclasses import dataclass
from .baseTag import BaseTag

@dataclass
class SubTag(BaseTag):

    sub:str = 'null'
    vip:str = 'null'
    mod:str = 'null'

    months:str = 'null'
    cumulative_months:str = 'null'
    multimonth_duration:str = 'null'
    multimonth_tenure:str = 'null'
    should_share_streak:str = 'null'

    sub_plan_name:str = 'null'
    sub_plan:str = 'null'
    was_gifted:str = 'null'

    #msg_id:str = 'null'
    #source_msg_id:str = 'null'