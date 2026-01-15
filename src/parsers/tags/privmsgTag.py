from dataclasses import dataclass
from .baseTag import BaseTag

@dataclass
class PrivmsgTag(BaseTag):

    returning_chatter:str = ''
    turbo:str = ''

    sub:str = ''
    vip:str = ''
    mod:str = ''

    reply_parent_msg_id:str = ''
    reply_parent_user_id:str = ''
    reply_parent_display_name:str = ''

    reply_thread_parent_user_id:str = ''
    reply_thread_parent_display_name:str = ''
    reply_thread_parent_msg_id:str = ''