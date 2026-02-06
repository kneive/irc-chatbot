from .baseTag import BaseTag
from dataclasses import dataclass

@dataclass
class ViewerMilestoneTag(BaseTag):
    
    param_category:str
    param_copoReward:int=-42
    param_id: str
    param_value:int=-42