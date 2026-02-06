from .announcementTag import AnnouncementTag
from .privmsgTag import PrivmsgTag
from .raidTag import RaidTag
from .roomstateTag import RoomstateTag
from .subgiftTag import SubgiftTag
from .submysteryTag import SubmysteryTag
from .subTag import SubTag
from .viewermilestoneTag import ViewerMilestoneTag
from .bitsbadgetierTag import BitsBadgeTierTag
from .onetapgiftTag import OnetapgiftTag
from .paidupgradeTag import PaidupgradeTag
from .payforwardTag import PayforwardTag

class TagFactory:
    # require room-name to be parsed explicitly


    @staticmethod
    def createAnnouncementTag(raw_tags:dict) -> AnnouncementTag:
        """Create tags for ANNOUNCEMENT messages"""

        return AnnouncementTag(user_id=raw_tags.get('user-id'),
                               display_name=raw_tags.get('display-name'),
                               login=raw_tags.get('login'),
                               badge_info=raw_tags.get('badge-info'),
                               badges=raw_tags.get('badges'),
                               source_badge_info=raw_tags.get('source-badges-info', None),
                               source_badges=raw_tags.get('source-badges', None),
                               turbo=-42,
                               returning_chatter=-42,
                               first_msg=-42,
                               color=raw_tags.get('color'),
                               emotes=raw_tags.get('emotes'),
                               flags=raw_tags.get('flags'),
                               user_type=raw_tags.get('user-type'),
                               room_id=raw_tags.get('room-id'),
                               source_room_id=raw_tags.get('source-room-id', None),
                               room_name=raw_tags.get('room-name', None),
                               id=raw_tags.get('id'),
                               msg_id=raw_tags.get('msg-id'),
                               source_msg_id=raw_tags.get('source-msg-id', None),
                               tmi_sent_ts=raw_tags.get('tmi-sent-ts'),
                               param_color=raw_tags.get('msg-param-color'),
                               system_msg=raw_tags.get('system-msg', None),
                               msg_content=raw_tags.get('message-content'))

    @staticmethod
    def createBitsBadgeTierTag(raw_tags:dict):
        """Create tags for BITSBADGETIER messages"""

        return BitsBadgeTierTag(room_name=raw_tags.get('room-name'),
                                room_id=raw_tags.get('room-id'),
                                source_room_id=raw_tags.get('source-room-id', None),
                                user_id=raw_tags.get('user-id'),
                                display_name=raw_tags.get('display-name'),
                                login=raw_tags.get('login'),
                                badge_info=raw_tags.get('badge-info'),
                                source_badge_info=raw_tags.get('source-badge-info', None),
                                badges=raw_tags.get('badges'),
                                source_badges=raw_tags.get('source-badges', None),
                                color=raw_tags.get('color'),
                                emotes=raw_tags.get('emotes'),
                                flags=raw_tags.get('flags'),
                                user_type=raw_tags.get('user-type'),
                                subscriber=int(raw_tags.get('subscriber', '0')),
                                vip=int(raw_tags.get('vip', '0')),
                                mod=int(raw_tags.get('mod', '0')),
                                msg_id=raw_tags.get('msg-id'),
                                source_msg_id=raw_tags.get('source-msg-id', None),
                                tmi_sent_ts=int(raw_tags.get('tmi-sent-ts')),
                                msg_param_threshold=int(raw_tags.get('msg-param-threshold')),
                                system_msg=raw_tags.get('system-msg'))

    @staticmethod
    def createCommunityPayforwardTag(raw_tags:dict):
        """Create tags for COMMUNITYPAYFORWARD messages"""

        return PayforwardTag(room_name=raw_tags.get('room-name'),
                             room_id=raw_tags.get('room-id'),
                             source_room_id=raw_tags.get('source-room-id', None),
                             user_id=raw_tags.get('user-id'),
                             display_name=raw_tags.get('display-name'),
                             login=raw_tags.get('login'),
                             badge_info=raw_tags.get('badge-info'),
                             source_badge_info=raw_tags.get('source-badge-info', None),
                             badges=raw_tags.get('badges'),
                             source_badges=raw_tags.get('source-badges', None),
                             color=raw_tags.get('color'),
                             emotes=raw_tags.get('emotes'),
                             flags=raw_tags.get('flags'),
                             user_type=raw_tags.get('user-type'),
                             subscriber=int(raw_tags.get('subscriber', '0')),
                             vip=int(raw_tags.get('vip', '0')),
                             mod=int(raw_tags.get('mod', '0')),
                             msg_id=raw_tags.get('msg-id'),
                             source_msg_id=raw_tags.get('source-msg-id', None),
                             tmi_sent_ts=int((raw_tags.get('tmi-sent-ts'))),
                             msg_param_prior_gifter_anonymous=raw_tags.get('msg-param-prior-gifter-anonymous'),
                             msg_param_prior_gifter_display_name=raw_tags.get('msg-param-prior-gifter-display-name'),
                             msg_param_prior_gifter_id=raw_tags.get('msg-param-prior-gifter-id'),
                             msg_param_prior_gifter_user_name=raw_tags.get('msg-param-prior-gifter-user-name'),
                             msg_param_recipient_display_name=raw_tags.get('msg-param-recipient-display-name', None),
                             msg_param_recipient_id=raw_tags.get('msg-param-recipient-id', None),
                             msg_param_recipient_user_name=raw_tags.get('msg-param-recipient-user-name', None),
                             system_msg=raw_tags.get('system-msg'))

    @staticmethod
    def createGiftPaidupgradeTag(raw_tags:dict):
        """Creatte tags for GIFTPAIDUPGRADE messages"""

        return PaidupgradeTags(room_name=raw_tags.get('room-name'),
                               room_id=raw_tags.get('room-id'),
                               source_room_id=raw_tags.get('source-room-id', None),
                               user_id=raw_tags.get('user-id'),
                               display_name=raw_tags.get('display-name'),
                               login=raw_tags.get('login'),
                               badge_info=raw_tags.get('badge-info'),
                               source_badge_info=raw_tags.get('source-badge-info', None),
                               badges=raw_tags.get('badges'),
                               source_badges=raw_tags.get('source-badges', None),
                               color=raw_tags.get('color'),
                               emotes=raw_tags.get('emotes'),
                               flags=raw_tags.get('flags'),
                               user_type=raw_tags.get('user-type'),
                               subscriber=int(raw_tags.get('subscriber', '0')),
                               vip=int(raw_tags.get('vip', '0')),
                               mod=int(raw_tags.get('mod', '0')),
                               msg_id=raw_tags.get('msg-id'),
                               source_msg_id=raw_tags.get('source-msg-id', None),
                               tmi_sent_ts=int(raw_tags.get('tmi-sent-ts')),
                               msg_param_sender_login=raw_tags.get('msg-param-sender-login'),
                               msg_param_sender_name=raw_tags.get('msg-param-sender-name'),
                               msg_param_sub_plan=raw_tags.get('msg-param-sub-plan'),
                               system_msg=raw_tags.get('system-msg'))

    @staticmethod
    def createOneTapGiftRedeemedTag(raw_tags:dict):
        """Create tags for ONETAPGIFTREDEEMED messages"""

        return OnetapgiftTag(room_name=raw_tags.get('room-name'),
                             room_id=raw_tags.get('room-id'),
                             source_room_id=raw_tags.get('source-room-id', None),
                             user_id=raw_tags.get('user-id'),
                             display_name=raw_tags.get('display-name'),
                             login=raw_tags.get('login'),
                             badge_info=raw_tags.get('badge-info'),
                             source_badge_info=raw_tags.get('source-badge-info', None),
                             badges=raw_tags.get('badges'),
                             source_badges=raw_tags.get('source-badges', None),
                             color=raw_tags.get('color'),
                             emotes=raw_tags.get('emotes'),
                             flags=raw_tags.get('flags'),
                             user_type=raw_tags.get('user-type'),
                             subscriber=int(raw_tags.get('subscriber', '0')),
                             vip=int(raw_tags.get('vip', '0')),
                             mod=int(raw_tags.get('mod', '0')),
                             msg_id=raw_tags.get('msg-id'),
                             source_msg_id=raw_tags.get('source-msg-id', None),
                             tmi_sent_ts=int(raw_tags.get('tmi-sent-ts')),
                             msg_param_bits_spent=int(raw_tags.get('msg-param-bits-spent', '0')),
                             msg_param_gift_id=raw_tags.get('msg-param-gift-id'),
                             msg_param_user_display_name=raw_tags.get('msg-param-user-display-name'),
                             system_msg=raw_tags.get('system-msg'))

    @staticmethod
    def createPrimePaidUpgradeTag(raw_tags:dict):
        """Create tags for PRIMEPAIDUPGRADE messages"""

        return PaidupgradeTag(room_name=raw_tags.get('room-name'),
                              room_id=raw_tags.get('room-id'),
                              source_room_id=raw_tags.get('source-room-id', None),
                              user_id=raw_tags.get('user-id'),
                              display_name=raw_tags.get('display-name'),
                              login=raw_tags.get('login'),
                              badge_info=raw_tags.get('badge-info'),
                              source_badge_info=raw_tags.get('source-badge-info', None),
                              badges=raw_tags.get('badges'),
                              source_badges=raw_tags.get('source-badges', None),
                              color=raw_tags.get('color'),
                              emotes=raw_tags.get('emotes'),
                              flags=raw_tags.get('flags'),
                              user_type=raw_tags.get('user-type'),
                              subscriber=int(raw_tags.get('subscriber', '0')),
                              vip=int(raw_tags.get('vip', '0')),
                              mod=int(raw_tags.get('mod', '0')),
                              msg_id=raw_tags.get('msg-id'),
                              source_msg_id=raw_tags.get('source-msg-id', None),
                              tmi_sent_ts=int(raw_tags.get('tmi-sent-ts')),
                              msg_param_sender_login=raw_tags.get('msg-param-sender-login'),
                              msg_param_sender_name=raw_tags.get('msg-param-sender-name'),
                              msg_param_sub_plan=raw_tags.get('msg-param-sub-plan'),
                              system_msg=raw_tags.get('system-msg'))

    @staticmethod
    def createPrivmsgTag(raw_tags: dict) -> PrivmsgTag:
        """Create tags for PRIVMSG messages"""

        return PrivmsgTag(room_name=raw_tags.get('room-name'),
                          room_id=raw_tags.get('room-id'),
                          source_room_id=raw_tags.get('source-room-id', None),
                          user_id=raw_tags.get('user-id'),
                          display_name=raw_tags.get('display-name'),
                          login=None,
                          badge_info=raw_tags.get('badge-info'),
                          source_badge_info=raw_tags.get('source-badge-info', None),
                          badges=raw_tags.get('badges'),
                          source_badges=raw_tags.get('source-badges', None),
                          color=raw_tags.get('color'),
                          emotes=raw_tags.get('emotes'),
                          flags=raw_tags.get('flags'),
                          user_type=raw_tags.get('user-type'),
                          subscriber=int(raw_tags.get('subscriber', '0')),
                          vip=int(raw_tags.get('vip', '0')),
                          mod=int(raw_tags.get('mod', '0')),
                          msg_id=raw_tags.get('msg-id'),
                          source_msg_id=raw_tags.get('source-msg-id', None),
                          tmi_sent_ts=int(raw_tags.get('tmi-sent-ts')),
                          message_id=raw_tags.get('id'),
                          source_message_id=raw_tags.get('source-id', None),
                          first_msg=int(raw_tags.get('first-msg', '0')),
                          returning_chatter=int(raw_tags.get('returning-chatter', '0')),
                          turbo=int(raw_tags.get('turbo', '0')),
                          msg_content=raw_tags.get('message-content'))
    
    @staticmethod
    def createRaidTag(raw_tags:dict) -> RaidTag:
        """Create tags for RAID messages"""
        
        return RaidTag(room_name=raw_tags.get('room-name'),
                       room_id=raw_tags.get('room-id'),
                       source_room_id=raw_tags.get('source-room-id', None),
                       user_id=raw_tags.get('user-id'),
                       display_name=raw_tags.get('display_name'),
                       login=raw_tags.get('login'),
                       badge_info=raw_tags.get('badge-info'),
                       source_badge_info=raw_tags.get('source-badge-info', None),
                       badges=raw_tags.get('badges'),
                       source_badges=raw_tags.get('source-badges', None),
                       color=raw_tags.get('color'),
                       emotes=raw_tags.get('emotes'),
                       flags=raw_tags.get('flags'),
                       user_type=raw_tags.get('user-type'),
                       subscriber=int(raw_tags.get('subscriber', '0')),
                       vip=int(raw_tags.get('vip', '0')),
                       mod=int(raw_tags.get('mod', '0')),
                       msg_id=raw_tags.get('msg-id'),
                       source_msg_id=raw_tags.get('source-msg-id', None),
                       tmi_sent_ts=int(raw_tags.get('tmi-sent-ts')),
                       msg_param_display_name=raw_tags.get('msg-param-display-name'),
                       msg_param_login=raw_tags.get('msg-param-login'),
                       msg_param_profileImageURL=raw_tags.get('msg-param-profileImageURL'),
                       msg_param_viewerCount=int(raw_tags.get('msg-param-viewerCount')),
                       system_msg=raw_tags.get('system-msg'))

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
    def createStandardPayForwardTag(raw_tags:dict):
        """Create tags for STANDARDPAYFORWARD messages"""

        return PayforwardTag(room_name=raw_tags.get('room-name'),
                             room_id=raw_tags.get('room-id'),
                             source_room_id=raw_tags.get('source-room-id', None),
                             user_id=raw_tags.get('user-id'),
                             display_name=raw_tags.get('display-name'),
                             login=raw_tags.get('login'),
                             badge_info=raw_tags.get('badge-info'),
                             source_badge_info=raw_tags.get('source-badge-info', None),
                             badges=raw_tags.get('badges'),
                             source_badges=raw_tags.get('source-badges', None),
                             color=raw_tags.get('color'),
                             emotes=raw_tags.get('emotes'),
                             flags=raw_tags.get('flags'),
                             user_type=raw_tags.get('user-type'),
                             subscriber=int(raw_tags.get('subscriber', '0')),
                             vip=int(raw_tags.get('vip', '0')),
                             mod=int(raw_tags.get('mod', '0')),
                             msg_id=raw_tags.get('msg-id'),
                             source_msg_id=raw_tags.get(',source-msg-id', None),
                             tmi_sent_ts=int(raw_tags.get('tmi-sent-ts')),
                             msg_param_prior_gifter_anonymous=raw_tags.get('msg-param-prior-gifter-anonymous'),
                             msg_param_prior_gifter_display_name=raw_tags.get('msg-param-prior-gifter-display-name'),
                             msg_param_prior_gifter_id=raw_tags.get('msg-param-prior-gifter-id'),
                             msg_param_prior_gifter_user_name=raw_tags.get('msg-param-prior-gifter-user-name'),
                             msg_param_recipient_display_name=raw_tags.get('msg-param-recipient-display-name'),
                             msg_param_recipient_id=raw_tags.get('msg-param-recipient-id'),
                             msg_param_recipient_user_name=raw_tags.get('msg-param-recipient-user-name'),
                             system_msg=raw_tags.get('system-msg'))

    @staticmethod
    def createSubgiftTag(raw_tags:dict) -> SubgiftTag:
        """Create tags for subgifts messages"""

        return SubgiftTag(room_name=raw_tags.get('room-name'),
                          room_id=raw_tags.get('room-id'),
                          source_room_id=raw_tags.get('source-room-id', None),
                          user_id=raw_tags.get('user-id'),
                          display_name=raw_tags.get('display-name'),
                          login=raw_tags.get('login'),
                          badge_info=raw_tags.get('badge-info'),
                          source_badge_info=raw_tags.get('source-badge-info', None),
                          badges=raw_tags.get('badges'),
                          source_badges=raw_tags.get('source-badges', None),
                          color=raw_tags.get('color'),
                          emotes=raw_tags.get('emotes'),
                          flags=raw_tags.get('flags'),
                          user_type=raw_tags.get('user-type'),
                          subscriber=int(raw_tags.get('subscriber', '0')),
                          vip=int(raw_tags.get('vip', '0')),
                          mod=int(raw_tags.get('mod', '0')),
                          msg_id=raw_tags.get('msg-id'),
                          source_msg_id=raw_tags.get('source-msg-id', None),
                          tmi_sent_ts=int(raw_tags.get('tmi-sent-ts')),
                          msg_param_community_gift_id=raw_tags.get('msg-param-community-gift-id'),
                          msg_param_fun_string=raw_tags.get('msg-param-fun-string'),
                          msg_param_gift_months=int(raw_tags.get('msg-param-gift-months')),
                          msg_param_months=int(raw_tags.get('msg-param-months')),
                          msg_param_origin_id=raw_tags.get('msg-param-origin-id'),
                          msg_param_recipient_displayu_name=raw_tags.get('msg-param-recipient-display-name'),
                          msg_param_recipient_id=raw_tags.get('msg-param-recipient-id'),
                          msg_param_recipient_user_name=raw_tags.get('msg-param-recipient-user-name'),
                          msg_param_sender_count=int(raw_tags.get('msg-param-sender-count')),
                          msg_param_sub_plan_name=raw_tags.get('msg-param-sub-plan-name'),
                          msg_param_sub_plan=raw_tags.get('msg-param-sub-plan'),
                          system_msg=raw_tags.get('system-msg'))
    
    @staticmethod
    def createSubmysterygiftTag(raw_tags:dict) -> SubmysteryTag:
        """Create tags for submysterygift messages"""

        return SubmysteryTag(room_name=raw_tags.get('room-name'),
                             room_id=raw_tags.get('room-id'),
                             source_room_id=raw_tags.get('source-room-id', None),
                             user_id=raw_tags.get('user-id'),
                             display_name=raw_tags.get('display-name'),
                             login=raw_tags.get('login'),
                             badge_info=raw_tags.get('badge-info'),
                             source_badge_info=raw_tags.get('source-badge-info', None),
                             badges=raw_tags.get('badges'),
                             source_badges=raw_tags.get('source-badges', None),
                             color=raw_tags.get('color'),
                             emotes=raw_tags.get('emotes'),
                             flags=raw_tags.get('flags'),
                             user_type=raw_tags.get('user-type'),
                             subscriber=int(raw_tags.get('subscriber', '0')),
                             vip=int(raw_tags.get('vip', '0')),
                             mod=int(raw_tags.get('mod', '0')),
                             msg_id=raw_tags.get('msg-id'),
                             source_msg_id=raw_tags.get('source-msg-id', None),
                             tmi_sent_ts=int(raw_tags.get('tmi-sent-ts')),
                             msg_param_community_gift_id=raw_tags.get('msg-param-community-gift-id'),
                             msg_param_mass_gift_count=int(raw_tags.get('msg-param-mass-gift-count', '0')),
                             msg_param_origin_id=raw_tags.get('msg-param-origin-id'),
                             msg_param_sender_count=int(raw_tags.get('msg-param-sender-count', '0')),
                             msg_param_sub_plan=raw_tags.get('msg-param-sub-plan'),
                             msg_param_goal_contribution_type=raw_tags.get('msg-param-goal-contribution-type'),
                             msg_param_goal_current_contributions=int(raw_tags.get('msg-param-goal-current-contributions', '0')),
                             msg_param_goal_target_contributions=int(raw_tags.get('msg-param-goal-target-contributions', '0')),
                             msg_param_goal_user_contributions=int(raw_tags.get('msg-param-goal-user-contributions', '0')),
                             system_msg=raw_tags.get('system-msg'))
    
    @staticmethod
    def createSubTag(raw_tags:dict) -> SubTag:
        """Create tags for sub messages"""

        return SubTag(room_name=raw_tags.get('room-name'),
                      room_id=raw_tags.get('room-id'),
                      source_room_id=raw_tags.get('source-room-id', None),
                      user_id=raw_tags.get('user-id'),
                      display_name=raw_tags.get('display-name'),
                      login=raw_tags.get('login'),
                      badge_info=raw_tags.get('badge-info'),
                      source_badge_info=raw_tags.get('source-badge-info', None),
                      badges=raw_tags.get('badges'),
                      source_badges=raw_tags.get('source-badges', None),
                      color=raw_tags.get('color'),
                      emotes=raw_tags.get('emotes'),
                      flags=raw_tags.get('flags'),
                      user_type=raw_tags.get('user-type'),
                      subscriber=int(raw_tags.get('subscriber', '0')),
                      vip=int(raw_tags.get('vip', '0')),
                      mod=int(raw_tags.get('mod', '0')),
                      msg_id=raw_tags.get('msg-id'),
                      source_msg_id=raw_tags.get('source-msg-id', None),
                      tmi_sent_ts=int(raw_tags.get('tmi-sent-ts')),
                      msg_param_cumulative_months=int(raw_tags.get('msg-param-cumulative-months', '0')),
                      msg_param_months=int(raw_tags.get('msg-param-months', '0')),
                      msg_param_multimonth_duration=int(raw_tags.get('msg-param-multimonth-duration', '0')),
                      msg_param_multimonth_tenure=int(raw_tags.get('msg-param-multimonth-tenure', '0')),
                      msg_param_should_share_streak=int(raw_tags.get('msg-param-should-share-streak', '0')),
                      msg_param_sub_plan_name=raw_tags.get('msg-param-sub-plan-name'),
                      msg_param_sub_plan=raw_tags.get('msg-param-sub-plan'),
                      msg_param_was_gifted=raw_tags.get('msg-param-was-gifted'),
                      system_msg=raw_tags.get('system-msg'))

    @staticmethod
    def createViewerMilestoneTag(raw_tags:dict) -> ViewerMilestoneTag:
        """Create tags for VIEWERMILESTONE messages"""

        return ViewerMilestoneTag(user_id=raw_tags.get('user-id'),
                                  display_name=raw_tags.get('display-name'),
                                  login=raw_tags.get('login'),
                                  badge_info=raw_tags.get('badge-info'),
                                  badges=raw_tags.get('badges'),
                                  source_badge_info=raw_tags.get('source-badge-info', None),
                                  source_badges=raw_tags.get('source-badges', None),
                                  turbo=-42,
                                  returning_chatter=-42,
                                  first_msg=-42,
                                  color=raw_tags.get('color'),
                                  emotes=raw_tags.get('emotes'),
                                  flags=raw_tags.get('flags'),
                                  user_type=raw_tags.get('user-type'),                                  
                                  room_id=raw_tags.get('room-id'),
                                  source_room_id=raw_tags.get('source-room-id', None),
                                  room_name='#unknown',
                                  id=raw_tags.get('id'),
                                  msg_id=raw_tags.get('msg-id'),
                                  source_msg_id=raw_tags.get('source-msg-id', None),
                                  tmi_sent_ts=raw_tags.get('tmi-sent-ts'),
                                  param_category=raw_tags.get('msg-param-category'),
                                  param_copoReward=int(raw_tags.get('msg-param-copoReward')),
                                  param_id=raw_tags.get('msg-param-id'),
                                  param_value=int(raw_tags.get('msg-param-value')),
                                  system_msg=raw_tags.get('system-msg'))