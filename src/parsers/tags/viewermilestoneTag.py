from .baseTag import BaseTag
from dataclasses import dataclass

@dataclass
class ViewerMilestoneTag(BaseTag):
    
    param_category:str | None = None
    param_copoReward:int=-42
    param_id: str | None = None
    param_value:int=-42
    system_msg:str | None = None