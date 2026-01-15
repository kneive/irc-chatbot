from .privmsgTag import PrivmsgTag
from .roomstateTag import RoomstateTag
from .subgiftTag import SubgiftTag
from .submysteryTag import SubmysterygiftTag
from .subTag import SubTag

class TagFactory:
    # require room-name to be parsed explicitly

    @staticmethod
    def createPrivmsgTag(raw_tags: dict) -> PrivmsgTag:
        """Create tags for PRIVMSG messages"""

        return PrivmsgTag(user_id=raw_tags.get('user-id'),
                          display_name=raw_tags.get('display-name'),
                          username=raw_tags.get('display-name').lower(),
                          badge_info=raw_tags.get('badge-info'),
                          badges=raw_tags.get('badges'),
                          source_badge_info=raw_tags.get('source-badge-info', 'null'),
                          source_badges=raw_tags.get('source-badges', 'null'),
                          color=raw_tags.get('color'),
                          emotes=raw_tags.get('emotes'),
                          flags=raw_tags.get('flags'),
                          user_type=raw_tags.get('user-type'),
                          room_id=raw_tags.get('room-id'),
                          source_room_id=raw_tags.get('source-room-id', 'null'),
                          room_name=raw_tags.get('room-name', '#unknown'),
                          id=raw_tags.get('id'),
                          tmi_sent_ts=raw_tags.get('tmi-sent-ts'),
                          returning_chatter=raw_tags.get('returning=chatter'),
                          turbo=raw_tags.get('turbo'),
                          sub=raw_tags.get('subscriber', '0'),
                          vip=raw_tags.get('vip', '0'),
                          mod=raw_tags.get('mod', '0'),
                          reply_parent_msg_id=raw_tags.get('reply-parent-msg-id'),
                          reply_parent_user_id=raw_tags.get('reply-parent-user-id'),
                          reply_parent_display_name=raw_tags.get('reply-parent-display-name'),
                          reply_thread_parent_user_id=raw_tags.get('reply-thread-parent-user-id'),
                          reply_thread_parent_display_name=raw_tags.get('reply-thread-parent-display-name'),
                          reply_thread_parent_msg_id=raw_tags.get('reply-thread-parent-msg-id'))
    
    @staticmethod
    def createRoomstateTag(raw_tags:dict) -> RoomstateTag:
        """Create tags for ROOMSTATE messages"""

        return RoomstateTag(room_name=raw_tags.get('room-name', '#unknown'),
                            emote_only=raw_tags.get('emotel-only', '-1'),
                            followers_only=raw_tags.get('followers-only', '-1'),
                            r9k=raw_tags.get('r9k', '-1'),
                            room_id=raw_tags.get('room-id'),
                            slow=raw_tags.get('slow', '-1'),
                            subs_only=raw_tags.get('subs-only', '-1'))
    
    @staticmethod
    def createSubgiftTag(raw_tags:dict) -> SubgiftTag:
        """Create tags for subgifts messages"""

        return SubgiftTag(user_id=raw_tags.get('user-id'),
                          display_name=raw_tags.get('display-name'),
                          username=raw_tags.get('display-name').lower(),
                          badge_info=raw_tags.get('badge-info'),
                          badges=raw_tags.get('badges'),
                          source_badge_info=raw_tags.get('source-badge-info', 'null'),
                          source_badges=raw_tags.get('source-badges', 'null'),
                          color=raw_tags.get('color'),
                          emotes=raw_tags.get('emotes'),
                          flags=raw_tags.get('flags'),
                          user_type=raw_tags.get('user-type'),
                          room_id=raw_tags.get('room-id'),
                          source_room_id=raw_tags.get('source-room-id', 'null'),
                          room_name=raw_tags.get('room-name', '#unknown'),
                          id=raw_tags.get('id'),
                          tmi_sent_ts=raw_tags.get('tmi-sent-ts'),
                          sub=raw_tags.get('subscriber', '0'),
                          vip=raw_tags.get('vip', '0'),
                          mod=raw_tags.get('mod', '0'),
                          gift_id=raw_tags.get('msg-param-community-get-id'),
                          origin_id=raw_tags.get('msg-param-origin-id'),
                          gift_moths=raw_tags.get('msg-param-gift-months'),
                          months=raw_tags.get('msg-param-months'),
                          recipient_id=raw_tags.get('msg-param-recipient-id'),
                          recipient_display_name=raw_tags.get('msg-param-recipient-display-name'),
                          recipient_username=raw_tags.get('msg-param-recipient-user-name'),
                          sender_count=raw_tags.get('msg-param-sender-count'),
                          sub_plan=raw_tags.get('msg-param-sub-plan'),
                          sub_plan_name=raw_tags.get('msg-param-sub-plan-name'),
                          msg_id=raw_tags.get('msg-id'),
                          source_msg_id=raw_tags.get('source-msg-id', 'null'))
    
    @staticmethod
    def createSubmysterygiftTag(raw_tags:dict) -> SubmysterygiftTag:
        """Create tags for submysterygift messages"""

        return SubmysterygiftTag(user_id=raw_tags.get('user-id'),
                                 display_name=raw_tags.get('display-name'),
                                 username=raw_tags.get('display-name').lower(),
                                 badge_info=raw_tags.get('badge-info'),
                                 badges=raw_tags.get('badges'),
                                 source_badge_info=raw_tags.get('source-badge-info', 'null'),
                                 source_badges=raw_tags.get('source-badges', 'null'),
                                 color=raw_tags.get('color'),
                                 emotes=raw_tags.get('emotes'),
                                 flags=raw_tags.get('flags'),
                                 user_type=raw_tags.get('user-type'),
                                 room_id=raw_tags.get('room-id'),
                                 source_room_id=raw_tags.get('source-room-id', 'null'),
                                 room_name=raw_tags.get('room-name', '#unknown'),
                                 id=raw_tags.get('id'),
                                 tmi_sent_ts=raw_tags.get('tmi-sent-ts'),
                                 sub=raw_tags.get('subscriber', '0'),
                                 vip=raw_tags.get('vip', '0'),
                                 mod=raw_tags.get('mod', '0'),
                                 gift_id=raw_tags.get('msg-param-community-gift-id'),
                                 origin_id=raw_tags.get('msg-param-origin-id'),
                                 sub_plan=raw_tags.get('msg-param-sub-plan'),
                                 mass_gift_count=raw_tags.get('msg-param-mass-gift-count'),
                                 sender_count=raw_tags.get('msg-param-sender-count'),
                                 msg_id=raw_tags.get('msg-id'),
                                 source_msg_id=raw_tags.get('source-msg-id', 'null'))
    
    @staticmethod
    def createSubTag(raw_tags:dict) -> SubTag:
        """Create tags for sub messages"""

        return SubTag(user_id=raw_tags.get('user-id'),
                      display_name=raw_tags.get('display-name'),
                      username=raw_tags.get('display-name').lower(),
                      badge_info=raw_tags.get('badge-info'),
                      badges=raw_tags.get('badges'),
                      source_badge_info=raw_tags.get('source-badge-info', 'null'),
                      source_badges=raw_tags.get('source-badges', 'null'),
                      color=raw_tags.get('color'),
                      emotes=raw_tags.get('emotes'),
                      flags=raw_tags.get('flags'),
                      user_type=raw_tags.get('user-type'),
                      room_id=raw_tags.get('room-id'),
                      source_room_id=raw_tags.get('source-room-id', 'null'),
                      room_name=raw_tags.get('room-name', '#unknown'),
                      id=raw_tags.get('id'),
                      tmi_sent_ts=raw_tags.get('tmi-sent-ts'),
                      sub=raw_tags.get('subscriber', '0'),
                      vip=raw_tags.get('vip', '0'),
                      mod=raw_tags.get('mod', '0'),
                      months=raw_tags.get('msg-param-months'),
                      cumulative_months=raw_tags.get('msg-param-cumulative-months'),
                      multimonth_duration=raw_tags.get('msg-param-multimonth-duration'),
                      multimonth_tenure=raw_tags.get('msg-param-multimonth-tenure'),
                      should_share_streak=raw_tags.get('msg-param-should-share-streak'),
                      sub_plan_name=raw_tags.get('msg-param-sub-plan-name'),
                      sub_plan=raw_tags.get('msg-param-sub-plan'),
                      was_gifted=raw_tags.get('msg-param-was-gifted'),
                      msg_id=raw_tags.get('msg-id'),
                      source_msg_id=raw_tags.get('source-msg-id', 'null'))