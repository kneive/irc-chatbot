from dataclasses import dataclass
from .baseTag import BaseTag

@dataclass
class OnetapgiftTag(BaseTag):

    # msg params
    msg_param_bits_spent:int=-42
    msg_param_gift_id:str
    msg_param_user_display_name:str

    # general
    system_msg:str