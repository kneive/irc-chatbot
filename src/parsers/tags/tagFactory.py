from .announcementTag import AnnouncementTag
from .privmsgTag import PrivmsgTag
from .raidTag import RaidTag
from .roomstateTag import RoomstateTag
from .subgiftTag import SubgiftTag
from .submysteryTag import SubmysterygiftTag
from .subTag import SubTag
from .viewermilestoneTag import ViewerMilestoneTag

class TagFactory:
    # require room-name to be parsed explicitly


    @staticmethod
    def createAnnouncementTag(raw_tags:dict) -> AnnouncementTag:
        """Create tags for ANNOUNCEMENT messages"""

        return AnnouncementTag(user_id=raw_tags.get('user-id'),
                               display_name=raw_tags.get('display-name'),
                               username=raw_tags.get('display-name').lower(),
                               badge_info=raw_tags.get('badge-info'),
                               badges=raw_tags.get('badges'),
                               source_badge_info=raw_tags.get('source-badges-info', 'null'),
                               source_badges=raw_tags.get('source-badges', 'null'),
                               turbo='-1',
                               returning_chatter='-1',
                               first_msg='-1',
                               color=raw_tags.get('color'),
                               emotes=raw_tags.get('emotes'),
                               flags=raw_tags.get('flags'),
                               user_type=raw_tags.get('user-type'),
                               room_id=raw_tags.get('room-id'),
                               source_room_id=raw_tags.get('source-room-id', 'null'),
                               room_name='#unknown',
                               id=raw_tags.get('id'),
                               msg_id=raw_tags.get('msg-id'),
                               source_msg_id=raw_tags.get('source-msg-id', 'null'),
                               tmi_sent_ts=raw_tags.get('tmi-sent-ts'),

                               param_color=raw_tags.get('msg-param-color'),
                               system_msg=raw_tags.get('system-msg', 'null'),
                               msg_content=raw_tags.get('null')
                               )

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
                          msg_id=raw_tags.get('msg-id'),
                          tmi_sent_ts=raw_tags.get('tmi-sent-ts'),
                          returning_chatter=raw_tags.get('returning-chatter', '-1'),
                          first_msg=raw_tags.get('first-msg', '-1'),
                          turbo=raw_tags.get('turbo', '-1'),
                          sub=raw_tags.get('subscriber', '-1'),
                          vip=raw_tags.get('vip', '-1'),
                          mod=raw_tags.get('mod', '-1'),
                          reply_parent_msg_id=raw_tags.get('reply-parent-msg-id', 'null'),
                          reply_parent_user_id=raw_tags.get('reply-parent-user-id', 'null'),
                          reply_parent_display_name=raw_tags.get('reply-parent-display-name', 'null'),
                          reply_thread_parent_user_id=raw_tags.get('reply-thread-parent-user-id', 'null'),
                          reply_thread_parent_display_name=raw_tags.get('reply-thread-parent-display-name', 'null'),
                          reply_thread_parent_msg_id=raw_tags.get('reply-thread-parent-msg-id', 'null'))
    
    @staticmethod
    def createRaidTag(raw_tags:dict) -> RaidTag:
        """Create tags for RAID messages"""
        
        return RaidTag(user_id=raw_tags.get('user-id'),
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
                       sub=raw_tags.get('subscriber', '-1'),
                       vip=raw_tags.get('vip', '-1'),
                       mod=raw_tags.get('mod', '-1'),
                       msg_param_displayName=raw_tags.get('msg-param-displayName', 'null'),
                       msg_param_lopgin=raw_tags.get('msg-param-login', 'null'),
                       msg_param_profileImageURL=raw_tags.get('msg-param-profileImageURL', 'null'),
                       msg_param_viewerCount=raw_tags.get('msg-param-viewerCount', '-1'),
                       msg_id=raw_tags.get('msg-id'),
                       source_msg_id=raw_tags.get('source-msg-id', 'null'),
                       msg_content=raw_tags.get('message-content', 'null'))

    @staticmethod
    def createRoomstateTag(raw_tags:dict) -> RoomstateTag:
        """Create tags for ROOMSTATE messages"""

        return RoomstateTag(room_id=raw_tags.get('room-id'),
                            emote_only=raw_tags.get('emote-only', '-1'),
                            followers_only=raw_tags.get('followers-only', '-1'),
                            r9k=raw_tags.get('r9k', '-1'),
                            slow_mode=raw_tags.get('slow', '-1'),
                            sub_only=raw_tags.get('subs-only', '-1'))
    
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
                          sub=raw_tags.get('subscriber', '-1'),
                          vip=raw_tags.get('vip', '-1'),
                          mod=raw_tags.get('mod', '-1'),
                          gift_id=raw_tags.get('msg-param-community-get-id'),
                          origin_id=raw_tags.get('msg-param-origin-id'),
                          gift_months=raw_tags.get('msg-param-gift-months'),
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
                                 sub=raw_tags.get('subscriber', '-1'),
                                 vip=raw_tags.get('vip', '-1'),
                                 mod=raw_tags.get('mod', '-1'),
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
                      sub=raw_tags.get('subscriber', '-1'),
                      vip=raw_tags.get('vip', '-1'),
                      mod=raw_tags.get('mod', '-1'),
                      months=raw_tags.get('msg-param-months'),
                      cumulative_months=raw_tags.get('msg-param-cumulative-months', '-1'),
                      multimonth_duration=raw_tags.get('msg-param-multimonth-duration', '-1'),
                      multimonth_tenure=raw_tags.get('msg-param-multimonth-tenure', '-1'),
                      should_share_streak=raw_tags.get('msg-param-should-share-streak', 'null'),
                      sub_plan_name=raw_tags.get('msg-param-sub-plan-name', 'null'),
                      sub_plan=raw_tags.get('msg-param-sub-plan'),
                      was_gifted=raw_tags.get('msg-param-was-gifted', 'null'),
                      msg_id=raw_tags.get('msg-id'),
                      source_msg_id=raw_tags.get('source-msg-id', 'null'))

    @staticmethod
    def createViewerMilestoneTag(raw_tags:dict) -> ViewerMilestoneTag:
        """Create tags for VIEWERMILESTONE messages"""

        return ViewerMilestoneTag(user_id=raw_tags.get('user-id'),
                                  display_name=raw_tags.get('display-name'),
                                  username=raw_tags.get('display-name').lower(),
                                  badge_info=raw_tags.get('badge-info'),
                                  badges=raw_tags.get('badges'),
                                  source_badge_info=raw_tags.get('source-badge-info', 'null'),
                                  source_badges=raw_tags.get('source-badges', 'null'),
                                  turbo='-1',
                                  returning_chatter='-1',
                                  first_msg='-1',
                                  color=raw_tags.get('color'),
                                  emotes=raw_tags.get('emotes'),
                                  flags=raw_tags.get('flags'),
                                  user_type=raw_tags.get('user-type'),                                  
                                  room_id=raw_tags.get('room-id'),
                                  source_room_id=raw_tags.get('source-room-id', 'null'),
                                  room_name='#unknown',
                                  id=raw_tags.get('id'),
                                  msg_id=raw_tags.get('msg-id'),
                                  source_msg_id=raw_tags.get('source-msg-id', 'null'),
                                  tmi_sent_ts=raw_tags.get('tmi-sent-ts'),
                                  
                                  param_category=raw_tags.get('msg-param-category'),
                                  param_copoReward=raw_tags.get('msg-param-copoReward'),
                                  param_id=raw_tags.get('msg-param-id'),
                                  param_value=raw_tags.get('msg-param-value'))