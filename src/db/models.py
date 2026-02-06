from dataclasses import dataclass

@dataclass
class Announcement:
    room_id:str | None = None
    user_id:str | None = None
    display_name:str | None = None
    msg_content:str | None = None

@dataclass
class Bits:
    user_id:str | None = None
    room_id:str | None = None
    source_room_id:str | None = None
    bits:int= -42

@dataclass
class Bitsbadgetier:
    room_id:str | None = None
    user_id:str | None = None
    msg_param_threshold:int=-42
    system_msg:str | None = None

@dataclass
class Onetapgift:
    user_id:str | None = None
    room_id:str | None = None
    tmi_sent_ts:str | None = None
    msg_id:str | None = None
    source_msg_id:str | None = None
    bits_spent:int | None = None
    gift_id:str | None = None
    user_display_name:str | None = None
    system_msg:str | None = None

@dataclass
class Payforward:
    user_id:str | None = None
    room_id:str | None = None
    tmi_sent_ts:str | None = None
    msg_id:str | None = None
    source_msg_id:str | None = None
    prior_gifter_anonymous:str | None = None
    prior_gifter_id:str | None = None
    prior_gifter_display_name:str | None = None
    prior_gifter_user_name:str | None = None
    recipient_id:str | None = None
    recipient_display_name:str | None = None
    recipient_user_name:str | None = None
    system_msg:str | None = None

@dataclass
class Paidupgrade:
    user_id:str | None = None
    room_id:str | None = None
    tmi_sent_ts:str | None = None
    msg_id:str | None = None
    source_msg_id:str | None = None
    sender_login:str | None = None
    sender_name:str | None = None
    sub_plan:str | None = None
    system_msg:str | None = None

@dataclass
class Privmsg:
    tmi_sent_ts:str | None = None
    message_id:str | None = None
    source_message_id:str | None = None
    room_id:str | None = None
    source_room_id:str | None = None
    user_id:str | None = None
    color:str | None = None
    returning_chatter:int=-42
    first_msg:int=-42
    flags:str | None = None
    emotes:str | None = None
    msg_content:str | None = None
    reply_parent_msg_body:str | None = None
    reply_parent_msg_id:str | None = None
    reply_parent_user_id:str | None = None
    reply_thread_parent_msg_id:str | None = None
    reply_thread_parent_user_id:str | None = None

@dataclass
class Raid:
    user_id:str | None = None
    room_id:str | None = None
    source_room_id:str | None = None
    tmi_sent_ts:str | None = None
    msg_id:str | None = None
    source_msg_id:str | None = None
    msg_param_displayName:str | None = None
    msg_param_login:str | None = None
    msg_param_profileImageURL:str | None = None
    msg_param_viewerCount:str | None = None
    system_msg:str | None = None

@dataclass
class Room:
    room_id:str | None = None
    room_name:str | None = None

@dataclass
class Roomstate:
    room_id:str | None = None
    emote_only:int=-42
    followers_only:int=-42
    r9k:int=-42
    slow_mode:int=-42
    sub_only:int=-42


@dataclass
class Sub:
    user_id:str | None = None
    room_id:str | None = None
    tmi_sent_ts:str | None = None
    msg_id:str | None = None
    source_msg_id:str | None = None
    cumulative_months:int=-42
    months:int=-42
    multimonth_duration:int=-42
    multimonth_tenure:int=-42
    should_share_streak:int=-42
    sub_plan_name:str | None = None
    sub_plan:str | None = None
    was_gifted:str | None = None
    system_msg:str | None = None

@dataclass
class Subgift:
    user_id:str | None = None
    room_id:str | None = None
    tmi_sent_ts:str | None = None
    msg_id:str | None = None
    source_msg_id:str | None = None
    community_gift_id:str | None = None
    fun_string:str | None = None
    gift_months:int=-42
    months:int=-42
    origin_id:str | None = None
    recipient_id:str | None = None
    recipient_display_name:str | None = None
    recipient_user_name:str | None = None
    sender_count:int=-42
    sub_plan_name:str | None = None
    sub_plan:str | None = None
    system_msg:str | None = None

@dataclass
class Submystery:
    user_id:str | None = None
    room_id:str | None = None
    tmi_sent_ts:str | None = None
    msg_id:str | None = None
    source_msg_id:str | None = None
    community_gift_id:str | None = None
    contribution_type:str | None = None
    current_contributions:int=-42
    target_contributions:int=-42
    user_contributions:int=-42
    mass_gift_count:int=-42
    origin_id:str | None = None
    sub_plan:str | None = None
    system_msg:str | None = None

@dataclass
class User:
    user_id:str | None = None
    login:str | None = None
    display_name:str | None = None
    user_type:str | None = None
    turbo:int=-42

@dataclass
class Userlist:
    room_name:str | None = None
    room_id:str | None = None
    username:str | None = None
    join_part:str | None = None

@dataclass
class UserRoom:
    user_id:str | None = None
    room_id:str | None = None
    badges:str | None = None
    badge_info:str | None = None
    subscriber:int=-42
    sub_streak:int=-42
    vip:int=-42
    mod:int=-42

@dataclass
class ViewerMilestone:
    room_id:str | None = None
    user_id:str | None = None
    display_name:str | None = None
    streak:int=-42
    system_msg:str | None = None