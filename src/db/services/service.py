
from ..repositories import (AnnouncementRepository,
                            BitsRepository,
                            BitsbadgetierRepository, 
                            OnetapgiftRepository,
                            PaidupgradeRepository,
                            PayforwardRepository,
                            PrivmsgRepository,
                            RaidRepository,
                            RoomRepository,
                            RoomStateRepository,
                            SubRepository,
                            SubgiftRepository,
                            SubmysteryRepository,
                            UserRepository,  
                            UserRoomRepository,
                            UserlistRepository,
                            ViewerMilestoneRepository)

from ..models import (Announcement,
                      Bits,
                      Bitsbadgetier,
                      Onetapgift,
                      Payforward,
                      Paidupgrade, 
                      Privmsg,
                      Raid, 
                      Room,
                      Roomstate, 
                      Sub, 
                      Subgift,
                      Submystery, 
                      User,
                      Userlist,
                      UserRoom, 
                      ViewerMilestone)

from parsers.tags import (AnnouncementTag, 
                          BaseTag,
                          BitsBadgeTierTag,
                          PaidupgradeTag,
                          PayforwardTag,
                          PrivmsgTag,
                          RaidTag, 
                          RoomstateTag,
                          OnetapgiftTag, 
                          SubgiftTag, 
                          SubmysteryTag,
                          SubTag, 
                          ViewerMilestoneTag)

from dataclasses import fields

MISSING_NUM = -1
MISSING_STR = 'null'

class SaltyService:

    def __init__(self,
                 announcement_repo: AnnouncementRepository,
                 bits_repo: BitsRepository,
                 bitsbadge_repo: BitsbadgetierRepository,
                 paidupgrade_repo: PaidupgradeRepository,
                 payforward_repo: PayforwardRepository,
                 privmsg_repo: PrivmsgRepository,
                 raid_repo: RaidRepository,
                 room_repo: RoomRepository,
                 roomstate_repo: RoomStateRepository,
                 onetap_repo: OnetapgiftRepository,
                 sub_repo: SubRepository,
                 subgift_repo: SubgiftRepository,
                 submystery_repo: SubmysteryRepository,
                 user_repo: UserRepository,
                 userRoom_repo: UserRoomRepository,
                 userlist_repo: UserlistRepository,
                 viewerMilestone_repo: ViewerMilestoneRepository):
        
        self.announcement_repo = announcement_repo
        self.bits_repo = bits_repo
        self.bitsbadge_repo = bitsbadge_repo
        self.onetap_repo = onetap_repo
        self.paidupgrade_repo = paidupgrade_repo
        self.payforward_repo = payforward_repo
        self.privmsg_repo = privmsg_repo
        self.raid_repo = raid_repo
        self.room_repo = room_repo
        self.roomstate_repo = roomstate_repo
        self.sub_repo = sub_repo
        self.subgift_repo = subgift_repo
        self.submystery_repo = submystery_repo
        self.user_repo = user_repo
        self.userRoom_repo = userRoom_repo
        self.userlist_repo = userlist_repo
        self.viewerMilestone_repo = viewerMilestone_repo

    def process_message(self, parsed: dict) -> None:
        """Process parsed message"""

        if not parsed.is_valid:
            print(f'PROCESS MESSAGE: Corrupted message: {parsed.error} (Variable: {parsed})')
            return
        
        if parsed.message_type == 'PRIVMSG':
            self._handlePrivmsg(parsed.data)
        elif parsed.message_type == 'SUBSCRIPTION':
            self._handleSubscription(parsed.data)
        elif parsed.message_type == 'SUBGIFT':
            self._handleSubgift(parsed.data)
        elif parsed.message_type == 'SUBMYSTERYGIFT':
            self._handleSubmysterygift(parsed.data)
        elif parsed.message_type == 'ANNOUNCEMENT':
            self._handleAnnouncement(parsed.data)
        elif parsed.message_type == 'VIEWERMILESTONE':
            self._handleViewerMilestone(parsed.data)
        elif parsed.message_type in ['JOIN', 'PART']:
            self._handleUserlist(parsed.data)
        elif parsed.message_type == 'ROOMSTATE':
            self._handleRoomstate(parsed.data)
        elif parsed.message_type == 'RAID':
            self._handleRaid(parsed.data)
        elif parsed.message_type in ['COMMUNITYPAYFORWARD', 'STANDARDPAYFORWARD']:
            self._handlePayforward(parsed.data)
        elif parsed.message_type in ['PRIMEPAIDUPGRADE', 'GIFTPAIDUPGRADE']:
            self._handlePaidupgrade(parsed.data)
        elif parsed.message_type == 'ONETAPGIFTREDEEMED':
            self._handleOnetapgift(parsed.data)
        elif parsed.message_type == 'BITSBADGETIER':
            self._handleBitsbadgetier(parsed.data)        


    def _handleAnnouncement(self, data:AnnouncementTag) -> None:
        """Handles ANNOUNCEMENT messages"""        

        self._checkUserRoomUserInRoom(data)

        if data.msg_id == 'sharedchatnotice':
            self.announcement_repo.save(Announcement(room_id=data.source_room_id,
                                                     user_id=data.user_id,
                                                     display_name=data.display_name,
                                                     msg_content=data.msg_content))
            
        else:
            self.announcement_repo.save(Announcement(room_id=data.room_id,
                                                     user_id=data.user_id,
                                                     display_name=data.display_name,
                                                     msg_content=data.msg_content))


    def _handleBitsbadgetier(self, data:BitsBadgeTierTag) -> None:
        """Handles BITSBADGETIER messages"""

        self._checkUserRoomUserInRoom(data)

        if data.msg_id == 'sharedchatnotice':
            self.bitsbadge_repo.save(Bitsbadgetier(room_id=data.source_room_id,
                                                   user_id=data.user_id,
                                                   msg_param_threshold=data.msg_param_threshold,
                                                   system_msg=data.system_msg))
        else:
            self.bitsbadge_repo.save(Bitsbadgetier(room_id=data.room_id,
                                                   user_id=data.user_id,
                                                   msg_param_threshold=data.msg_param_threshold,
                                                   system_msg=data.system_msg))

    def _handleOnetapgift(self, data:OnetapgiftTag) -> None:
        """Handles ONETAPGIFTREDEEMED messages"""

        self._checkUserRoomUserInRoom(data)

        if data.msg_id == 'sharedchatnotice':

            self.onetap_repo.save(Onetapgift(user_id=data.user_id,
                                            room_id=data.source_room_id,
                                            tmi_sent_ts=data.tmi_sent_ts,
                                            msg_id=data.msg_id,
                                            source_msg_id=data.source_msg_id,
                                            bits_spent=data.msg_param_bits_spent,
                                            gift_id=data.msg_param_gift_id,
                                            user_display_name=data.msg_param_user_display_name,
                                            system_msg=data.system_msg))

        else:

            self.onetap_repo.save(Onetapgift(user_id=data.user_id,
                                            room_id=data.room_id,
                                            tmi_sent_ts=data.tmi_sent_ts,
                                            msg_id=data.msg_id,
                                            source_msg_id=data.source_msg_id,
                                            bits_spent=data.msg_param_bits_spent,
                                            gift_id=data.msg_param_gift_id,
                                            user_display_name=data.msg_param_user_display_name,
                                            system_msg=data.system_msg))


    def _handlePaidupgrade(self, data:PaidupgradeTag) -> None:
        """Handles PRIMEPAIDUPGRADE and GIFTPAIDUPGRADE messages"""

        self._checkUserRoomUserInRoom(data)

        if data.msg_id == 'sharedchatnotice':

            self.paidupgrade_repo.save(Paidupgrade(user_id=data.user_id,
                                                   room_id=data.source_room_id,
                                                   tmi_sent_ts=data.tmi_sent_ts,
                                                   msg_id=data.msg_id,
                                                   source_msg_id=data.source_msg_id,
                                                   sender_login=data.msg_param_sender_login,
                                                   sender_name=data.msg_param_sender_name,
                                                   sub_plan=data.msg_param_sub_plan,
                                                   system_msg=data.system_msg))

        else:

            self.paidupgrade_repo.save(Paidupgrade(user_id=data.user_id,
                                                   room_id=data.room_id,
                                                   tmi_sent_ts=data.tmi_sent_ts,
                                                   msg_id=data.msg_id,
                                                   source_msg_id=data.source_msg_id,
                                                   sender_login=data.msg_param_sender_login,
                                                   sender_name=data.msg_param_sender_name,
                                                   sub_plan=data.msg_param_sub_plan,
                                                   system_msg=data.system_msg))

    def _handlePayforward(self, data:PayforwardTag) -> None:
        """Handles COMMUNITYPAYFORWARD and STANDARDPAYFORWARD messages"""

        self._checkUserRoomUserInRoom(data)

        if data.msg_id == 'sharedchatnotice':

            self.payforward_repo.save(Payforward(user_id=data.user_id,
                                                 room_id=data.source_room_id,
                                                 tmi_sent_ts=data.tmi_sent_ts,
                                                 msg_id=data.msg_id,
                                                 source_msg_id=data.source_msg_id,
                                                 prior_gifter_anonymous=data.msg_param_prior_gifter_anonymous,
                                                 prior_gifter_id=data.msg_param_prior_gifter_id,
                                                 prior_gifter_display_name=data.msg_param_prior_gifter_display_name,
                                                 prior_gifter_user_name=data.msg_param_prior_gifter_user_name,
                                                 recipient_id=data.msg_param_recipient_id,
                                                 recipient_display_name=data.msg_param_recipient_display_name,
                                                 recipient_user_name=data.msg_param_recipient_user_name,
                                                 system_msg=data.system_msg))

        else:

            self.payforward_repo.save(Payforward(user_id=data.user_id,
                                                 room_id=data.room_id,
                                                 tmi_sent_ts=data.tmi_sent_ts,
                                                 msg_id=data.msg_id,
                                                 source_msg_id=data.source_msg_id,
                                                 prior_gifter_anonymous=data.msg_param_prior_gifter_anonymous,
                                                 prior_gifter_id=data.msg_param_prior_gifter_id,
                                                 prior_gifter_display_name=data.msg_param_prior_gifter_display_name,
                                                 prior_gifter_user_name=data.msg_param_prior_gifter_user_name,
                                                 recipient_id=data.msg_param_recipient_id,
                                                 recipient_display_name=data.msg_param_recipient_display_name,
                                                 recipient_user_name=data.msg_param_recipient_user_name,
                                                 system_msg=data.system_msg))

    def _handlePrivmsg(self, data:PrivmsgTag) -> None:
        """Handles Priv messages"""

        self._checkUserRoomUserInRoom(data)

        self._checkReplyThread(data)

        if data.bits != -42:

            self.bits_repo.save(Bits(user_id=data.user_id,
                                     room_id=data.room_id,
                                     source_room_id=data.source_room_id,
                                     bits=data.bits))

        self.privmsg_repo.save(Privmsg(tmi_sent_ts=data.tmi_sent_ts,
                                        message_id=data.message_id,
                                        source_message_id=data.source_message_id,
                                        room_id=data.room_id,
                                        source_room_id=data.source_room_id,
                                        user_id=data.user_id,
                                        color=data.color,
                                        returning_chatter=data.returning_chatter,
                                        first_msg=data.first_msg,
                                        flags=data.flags,
                                        emotes=data.emotes,
                                        msg_content=data.msg_content,
                                        reply_parent_user_id=data.reply_parent_user_id,
                                        reply_parent_msg_id=data.reply_parent_msg_id,
                                        reply_parent_msg_body=data.reply_parent_msg_body,
                                        reply_thread_parent_user_id=data.reply_thread_parent_user_id,
                                        reply_thread_parent_msg_id=data.reply_thread_parent_msg_id))

    def _handleRaid(self, data:RaidTag) -> None:
        """Handles RAID messages"""

        self._checkUserRoomUserInRoom(data)
        # custom check for room and user

        self.raid_repo.save(Raid(user_id=data.user_id,
                                    room_id=data.room_id,
                                    source_room_id=data.source_room_id,
                                    tmi_sent_ts=data.tmi_sent_ts,
                                    msg_id=data.msg_id,
                                    source_msg_id=data.source_msg_id,
                                    msg_param_displayName=data.msg_param_display_name,
                                    msg_param_login=data.msg_param_login,
                                    msg_param_profileImageURL=data.msg_param_profileImageURL,
                                    msg_param_viewerCount=data.msg_param_viewerCount,
                                    system_msg=data.system_msg))
    
    def _handleRoomstate(self, data:RoomstateTag) -> None:
        """Handles ROOMSTATE messages"""

        if self.roomstate_repo.exists(room_id=data.room_id):
            roomstate = self.roomstate_repo.get_by_id(room_id=data.room_id)

            for f in fields(data):
                key = f.name
                value = getattr(data, key)

                if value == '-1':
                    setattr(data, key, getattr(roomstate, key))

        self.roomstate_repo.save(Roomstate(room_id=data.room_id,
                                           followers_only=data.followers_only,
                                           sub_only=data.sub_only,
                                           emote_only=data.emote_only,
                                           slow_mode=data.slow_mode,
                                           r9k=data.r9k))

    def _handleSubscription(self, data:SubTag) -> None:
        """Handles SUB messages"""

        self._checkUserRoomUserInRoom(data)

        if data.msg_id == 'sharedchatnotice':
    
            self.sub_repo.save(Sub(user_id=data.user_id,
                                   room_id=data.source_room_id,
                                   tmi_sent_ts=data.tmi_sent_ts,
                                   msg_id=data.msg_id,
                                   source_msg_id=data.source_msg_id,
                                   cumulative_months=data.msg_param_cumulative_months,
                                   months=data.msg_param_months,
                                   multimonth_duration=data.msg_param_multimonth_duration,
                                   multimonth_tenure=data.msg_param_multimonth_tenure,
                                   should_share_streak=data.msg_param_should_share_streak,
                                   sub_plan_name=data.msg_param_sub_plan_name,
                                   sub_plan=data.msg_param_sub_plan,
                                   was_gifted=data.msg_param_was_gifted,
                                   system_msg=data.system_msg))
            
        else:
            
            self.sub_repo.save(Sub(user_id=data.user_id,
                                   room_id=data.room_id,
                                   tmi_sent_ts=data.tmi_sent_ts,
                                   msg_id=data.msg_id,
                                   source_msg_id=data.source_msg_id,
                                   cumulative_months=data.msg_param_cumulative_months,
                                   months=data.msg_param_months,
                                   multimonth_duration=data.msg_param_multimonth_duration,
                                   multimonth_tenure=data.msg_param_multimonth_tenure,
                                   should_share_streak=data.msg_param_should_share_streak,
                                   sub_plan_name=data.msg_param_sub_plan_name,
                                   sub_plan=data.msg_param_sub_plan,
                                   was_gifted=data.msg_param_was_gifted,
                                   system_msg=data.system_msg))


    def _handleSubgift(self, data:SubgiftTag) -> None:
        """Handles SUBGIFT messages"""

        self._checkUserRoomUserInRoom(data)

        if data.msg_id == 'sharedchatnotice':

            self.subgift_repo.save(Subgift(user_id=data.user_id,
                                           room_id=data.source_room_id,
                                           tmi_sent_ts=data.tmi_sent_ts,
                                           msg_id=data.msg_id,
                                           source_msg_id=data.source_msg_id,
                                           community_gift_id=data.msg_param_community_gift_id,
                                           fun_string=data.msg_param_fun_string,
                                           gift_months=data.msg_param_gift_months,
                                           months=data.msg_param_months,
                                           origin_id=data.msg_param_origin_id,
                                           recipient_id=data.msg_param_recipient_id,
                                           recipient_display_name=data.msg_param_recipient_display_name,
                                           recipient_user_name=data.msg_param_recipient_user_name,
                                           sender_count=data.msg_param_sender_count,
                                           sub_plan_name=data.msg_param_sub_plan_name,
                                           sub_plan=data.msg_param_sub_plan,
                                           system_msg=data.system_msg))

        else:

            self.subgift_repo.save(Subgift(user_id=data.user_id,
                                           room_id=data.room_id,
                                           tmi_sent_ts=data.tmi_sent_ts,
                                           msg_id=data.msg_id,
                                           source_msg_id=data.source_msg_id,
                                           community_gift_id=data.msg_param_community_gift_id,
                                           fun_string=data.msg_param_fun_string,
                                           gift_months=data.msg_param_gift_months,
                                           months=data.msg_param_months,
                                           origin_id=data.msg_param_origin_id,
                                           recipient_id=data.msg_param_recipient_id,
                                           recipient_display_name=data.msg_param_recipient_display_name,
                                           recipient_user_name=data.msg_param_recipient_user_name,
                                           sender_count=data.msg_param_sender_count,
                                           sub_plan_name=data.msg_param_sub_plan_name,
                                           sub_plan=data.msg_param_sub_plan,
                                           system_msg=data.system_msg))

    def _handleSubmysterygift(self, data:SubmysteryTag) -> None:
        """Handles SUBMYSTERYGIFT messages"""

        self._checkUserRoomUserInRoom(data)

        if data.msg_id == 'sharedchatnotice':

            self.submystery_repo.save(Submystery(user_id=data.user_id,
                                                 room_id=data.source_room_id,
                                                 tmi_sent_ts=data.tmi_sent_ts,
                                                 msg_id=data.msg_id,
                                                 source_msg_id=data.source_msg_id,
                                                 community_gift_id=data.msg_param_community_gift_id,
                                                 contribution_type=data.msg_param_goal_contribution_type,
                                                 current_contributions=data.msg_param_goal_current_contributions,
                                                 target_contributions=data.msg_param_goal_target_contributions,
                                                 user_contributions=data.msg_param_goal_user_contributions,
                                                 mass_gift_count=data.msg_param_mass_gift_count,
                                                 origin_id=data.msg_param_origin_id,
                                                 sub_plan=data.msg_param_sub_plan,
                                                 system_msg=data.system_msg))

        else:

            self.submystery_repo.save(Submystery(user_id=data.user_id,
                                                 room_id=data.room_id,
                                                 tmi_sent_ts=data.tmi_sent_ts,
                                                 msg_id=data.msg_id,
                                                 source_msg_id=data.source_msg_id,
                                                 community_gift_id=data.msg_param_community_gift_id,
                                                 contribution_type=data.msg_param_goal_contribution_type,
                                                 current_contributions=data.msg_param_goal_current_contributions,
                                                 target_contributions=data.msg_param_goal_target_contributions,
                                                 user_contributions=data.msg_param_goal_user_contributions,
                                                 mass_gift_count=data.msg_param_mass_gift_count,
                                                 origin_id=data.msg_param_origin_id,
                                                 sub_plan=data.msg_param_sub_plan,
                                                 system_msg=data.system_msg))
            

    def _handleUserlist(self, data:dict) -> None:

        # handles JOIN and PART
        if self.room_repo.exists_by_name(room_name=data.get('room-name')):
            data['room-id'] = self.room_repo.get_by_name(room_name=data.get('room-name'))

        self.userlist_repo.save(Userlist(room_name=data.get('room-name'),
                                            room_id=data.get('room-id', None),
                                            username=data.get('display-name'),
                                            join_part=data.get('msg-type')))


    def _handleViewerMilestone(self, data:ViewerMilestoneTag) -> None:
        """Handles VIEWERMILESTONE messagers"""

        self._checkUserRoomUserInRoom(data)

        if data.msg_id == 'sharedchatnotice':
            self.viewerMilestone_repo.save(ViewerMilestone(room_id=data.source_room_id,
                                                           user_id=data.user_id,
                                                           display_name=data.display_name,
                                                           streak=data.param_value,
                                                           system_msg=data.system_msg))
            
        else:
            self.viewerMilestone_repo.save(ViewerMilestone(room_id=data.room_id,
                                                           user_id=data.user_id,
                                                           display_name=data.display_name,
                                                           streak=data.param_value,
                                                           system_msg=data.system_msg))


# Helpers

    def _checkUserRoomUserInRoom(self, data:BaseTag) -> None:

        if data.msg_id == 'sharedchatnotice':

            # extract substreak
            if data.badges:
                badges = data.badges.split(',')
                for badge in badges:
                    if badge.startswith('subscriber'):
                        data.sub_streak = int(badge.split('/')[1])

            if not self.user_repo.exists(user_id=data.user_id):
            
                # check whether user exists in user table
                self.user_repo.save(User(user_id=data.user_id,
                                         login=data.login,
                                         display_name=data.display_name,
                                         user_type=data.user_type,
                                         turbo=data.turbo))

            # check whether room and source-room exist in room table
            if not self.room_repo.exists(room_id=data.source_room_id):

                self.room_repo.save(Room(room_id=data.source_room_id,
                                         room_name=data.source_room_name))
            
            if not self.room_repo.exists(room_id=data.room_id):
                
                self.room_repo.save(Room(room_id=data.room_id,
                                         room_name=data.room_name))


            # check whether user exists in user_in_room table
            if not self.userRoom_repo.exists(room_id=data.source_room_id, user_id=data.user_id):

                self.userRoom_repo.save(UserRoom(user_id=data.user_id,
                                                 room_id=data.source_room_id,
                                                 badges=data.source_badges,
                                                 badge_info=data.source_badge_info,
                                                 subscriber=data.subscriber,
                                                 sub_streak=data.sub_streak,
                                                 vip=data.vip,
                                                 mod=data.mod))
        
        else:

            # check whether user exists in user table
            if not self.user_repo.exists(user_id=data.user_id):
                
                self.user_repo.save(User(user_id=data.user_id,
                                         login=data.login,
                                         display_name=data.display_name,
                                         user_type=data.user_type,
                                         turbo=data.turbo))

            # check whether room and source-room exist in room table
            if not self.room_repo.exists(room_id=data.room_id):

                self.room_repo.save(Room(room_id=data.room_id,
                                         room_name=data.room_name))


            # check whether user exists in user_in_room table
            if not self.userRoom_repo.exists(room_id=data.room_id, user_id=data.user_id):
                
                self.userRoom_repo.save(UserRoom(user_id=data.user_id,
                                                 room_id=data.room_id,
                                                 badges=data.badges,
                                                 badge_info=data.badge_info,
                                                 subscriber=data.subscriber,
                                                 sub_streak=data.sub_streak,
                                                 vip=data.vip,
                                                 mod=data.mod))
    
    def _checkReplyThread(self, data:PrivmsgTag) -> None:

        if data.reply_thread_parent_user_id is not None:
            if not self.user_repo.exists(user_id=data.reply_thread_parent_user_id):
                self.user_repo.save(User(user_id=data.reply_thread_parent_user_id,
                                        login=data.reply_thread_parent_user_login,
                                        display_name=data.reply_thread_parent_display_name,
                                        user_type=None,
                                        turbo=-42))

        if data.reply_parent_user_id is not None:    
            if not self.user_repo.exists(user_id=data.reply_parent_user_id):
                self.user_repo.save(User(user_id=data.reply_parent_user_id,
                                         login=data.reply_parent_user_login,
                                         display_name=data.reply_parent_display_name,
                                         user_type=None,
                                         turbo=-42))