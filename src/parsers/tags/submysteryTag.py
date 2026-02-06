from dataclasses import dataclass
from .baseTag import BaseTag

@dataclass
class SubmysteryTag(BaseTag):

    # msg params
    msg_param_community_gift_id:str | None = None
    msg_param_mass_gift_count:int=-42
    msg_param_origin_id:str | None = None
    msg_param_sender_count:int=-42
    msg_param_sub_plan:str | None = None
    msg_param_goal_contribution_type:str | None = None
    msg_param_goal_current_contributions:int=-42
    msg_param_goal_target_contributions:int=-42
    msg_param_goal_user_contributions:int=-42

    # general
    system_msg:str | None = None