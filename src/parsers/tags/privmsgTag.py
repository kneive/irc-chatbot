from dataclasses import dataclass
from .baseTag import BaseTag

@dataclass
class PrivmsgTag(BaseTag):

    #returning_chatter:str = 'null'
    #first_msg:str = 'null'
    #turbo:str = 'null'

    sub:str = 'null'
    vip:str = 'null'
    mod:str = 'null'

    reply_parent_msg_id:str = 'null'
    reply_parent_user_id:str = 'null'
    reply_parent_display_name:str = 'null'

    reply_thread_parent_user_id:str = 'null'
    reply_thread_parent_display_name:str = 'null'
    reply_thread_parent_msg_id:str = 'null'

    #msg_id:str = 'null'
    message_content:str = 'null'