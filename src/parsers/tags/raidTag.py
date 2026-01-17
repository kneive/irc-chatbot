from dataclasses import dataclass
from .baseTag import BaseTag

@dataclass
class RaidTag(BaseTag):

    msg_param_displayName:str = 'null'
    msg_param_login:str = 'null'
    msg_param_profileImageURL:str = 'null'
    msg_param_viewerCount:str = '-1'

    # additional fields
    msg_content:str = 'null'