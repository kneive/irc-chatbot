from dataclasses import dataclass
from .baseTag import BaseTag

@dataclass
class BitsBadgeTierTag(BaseTag):

    # msg params 
    msg_param_threshold:int=-42

    # general
    system_msg:str | None = None