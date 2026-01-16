from .baseTag import BaseTag
from dataclasses import dataclass

@dataclass
class ViewerMilestoneTag(BaseTag):
    
    param_category:str = 'null'
    param_copoReward:str = '-1'
    param_id: str = 'null'
    param_value:str = '-1'