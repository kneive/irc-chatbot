from dataclasses import dataclass
from .baseTag import BaseTag

@dataclass
class PrivmsgTag(BaseTag):

    bits:int=-42   
    message_id:str | None = None
    source_message_id:str | None = None
    first_msg:int=-42
    returning_chatter:int=-42
    msg_content:str | None = None

    reply_parent_display_name:str | None = None
    reply_parent_msg_body:str | None = None
    reply_parent_msg_id:str | None = None
    reply_parent_user_id:str | None = None
    reply_parent_user_login:str | None = None
    reply_thread_parent_display_name:str | None = None
    reply_thread_parent_msg_id:str | None = None
    reply_thread_parent_user_id:str | None = None
    reply_thread_parent_user_login:str | None = None
