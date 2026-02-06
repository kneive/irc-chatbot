from dataclasses import dataclass

@dataclass
class Announcement:
    room_id:str
    user_id:str
    display_name:str
    msg_content:str

@dataclass
class Bitsbadgetier:
    room_id:str
    user_id:str
    msg_param_threshold:int=-42
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
class Privmsg:
    tmi_sent_ts:str
    message_id:str
    source_message_id:str
    room_id:str
    source_room_id:str
    user_id:str
    color:str
    returning_chatter:int=-42
    first_msg:int=-42
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
class Room:
    room_id:str
    room_name:str

@dataclass
class Roomstate:
    room_id:str
    emote_only:int=-42
    followers_only:int=-42
    r9k:int=-42
    slow:int=-42
    subs_only:int=-42


@dataclass
class Sub:
    user_id:str
    room_id:str
    tmi_sent_ts:str
    msg_id:str
    source_msg_id:str
    cumulative_months:int=-42
    months:int=-42
    multimonth_duration:int=-42
    multimonth_tenure:int=-42
    should_share_streak:int=-42
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
    gift_months:int=-42
    months:int=-42
    origin_id:str
    recipient_id:str
    recipient_display_name:str
    recipient_user_name:str
    sender_count:int=-42
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
    current_contributions:int=-42
    target_contributions:int=-42
    user_contributions:int=-42
    mass_gift_count:int=-42
    origin_id:str
    sub_plan:str
    system_msg:str

@dataclass
class User:
    user_id:str
    login:str
    display_name:str
    user_type:str
    turbo:int=-42

@dataclass
class Userlist:
    room_name:str
    room_id:str
    username:str
    join_part:str

@dataclass
class UserRoom:
    user_id:str
    room_id:str
    badges:str
    bade_info:str
    subscriber:int=-42
    sub_streak:int=-42
    vip:int=-42
    mod:int=-42

@dataclass
class ViewerMilestone:
    room_id:str
    user_id:str
    display_name:str
    streak:int=-42