from dataclasses import dataclass

@dataclass
class User:
    user_id:str
    login:str
    display_name:str
    user_type:str
    turbo:int

@dataclass
class Room:
    room_id:str
    room_name:str

@dataclass
class UserRoom:
    user_id:str
    room_id:str
    badges:str
    bade_info:str
    subscriber:int
    sub_streak:int
    vip:int
    mod:int

@dataclass
class Privmsg:
    tmi_sent_ts:str
    message_id:str
    source_message_id:str
    room_id:str
    source_room_id:str
    user_id:str
    color:str
    returning_chatter:int
    first_msg:int
    flags:str
    emotes:str
    msg_content:str

@dataclass
class Raid:
    user_id:str
    room_id:str
    tmi_sent_ts:str
    msg_id:str
    msg_param_displayName:str
    msg_param_login:str
    msg_param_profileImageURL:str
    msg_param_viewerCount:str
    system_msg:str

@dataclass
class Sub:
    user_id:str
    room_id:str
    tmi_sent_ts:str
    msg_id:str
    source_msg_id:str
    cumulative_months:int
    months:int
    multimonth_duration:int
    multimonth_tenure:int
    should_share_streak:int
    sub_plan_name:str
    sub_plan:str
    was_gifted:str
    system_msg:str

@dataclass
class Subgift:
    user_id:str
    room_id:str
    tmi_sent_ts:str
    msg_id:str
    source_msg_id:str
    community_gift_id:str
    fun_string:str
    gift_months:int
    months:int
    origin_id:str
    recipient_id:str
    recipient_display_name:str
    recipient_user_name:str
    sender_count:int
    sub_plan_name:str
    sub_plan:str
    system_msg:str

@dataclass
class Submystery:
    user_id:str
    room_id:str
    tmi_sent_ts:str
    msg_id:str
    source_msg_id:str
    community_gift_id:str
    contribution_type:str
    current_contributions:int
    target_contributions:int
    user_contributions:int
    mass_gift_count:int
    origin_id:str
    sub_plan:str
    system_msg:str

@dataclass
class Payforward:
    user_id:str
    room_id:str
    tmi_sent_ts:str
    msg_id:str
    source_msg_id:str
    prior_gifter_anonymous:str
    prior_gifter_id:str
    prior_gifter_display_name:str
    prior_gifter_user_name:str
    recipient_id:str
    recipient_display_name:str
    recipient_user_name:str
    system_msg:str

@dataclass
class Paidupgrade:
    user_id:str
    room_id:str
    tmi_sent_ts:str
    msg_id:str
    source_msg_id:str
    sender_login:str
    sender_name:str
    sub_plan:str
    system_msg:str

@dataclass
class Onetapgift:
    user_id:str
    room_id:str
    tmi_sent_ts:str
    msg_id:str
    source_msg_id:str
    bits_spent:int
    gift_id:str
    user_display_name:str
    system_msg:str

@dataclass
class Roomstate:
    room_id:str
    emote_only:int
    followers_only:int
    r9k:int
    slow:int
    subs_only:int

@dataclass
class Userlist:
    room_name:str
    room_id:str
    username:str
    join_part:str