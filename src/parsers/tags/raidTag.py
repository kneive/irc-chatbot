from dataclasses import dataclass
from .baseTag import BaseTag

@dataclass
class RaidTag(BaseTag):

    # raid (not in unraid)
    msg_param_display_name:str
    msg_param_login:str
    msg_param_profileImageURL:str
    msg_param_viewerCount:int=-42

    # general
    system_msg:str