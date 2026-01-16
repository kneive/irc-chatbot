from dataclasses import dataclass
from .baseTag import BaseTag

@dataclass
class SubTag(BaseTag):

    months:str = '-1'
    cumulative_months:str = '-1'
    multimonth_duration:str = '-1'
    multimonth_tenure:str = '-1'
    should_share_streak:str = 'null'

    sub_plan_name:str = 'null'
    sub_plan:str = 'null'
    was_gifted:str = '-1'

    #unused (found in resub, gifted=true, anon-gift=true)
    #msg-param-anon-gift:str = 'null'
    #msg-param-gift-month-being0redeemed:str = '-1'
    #msg-param-gift-months:str = '-1'