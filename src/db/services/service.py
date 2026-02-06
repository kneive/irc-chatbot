
from ..repositories import (AnnouncementRepository,
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
        elif parsed.message_type == ['COMMUNITYPAYFORWARD', 'STANDARDPAYFORWARD']:
            self._handlePayforward(parsed.data)
        elif parsed.message_type == ['PRIMEPAIDUPGRADE', 'GIFTPAIDUPGRADE']:
            self._handlePaidupgrade(parsed.data)
        elif parsed.message_type == 'ONETAPGIFTREDEEMED':
            self._handleOnetapgift(parsed.data)
        # elif parsed.message_type == 'BITSBADGETIER': no table and repository        


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


    # _handlebitsbadge

    def _handleOnetapgift(self, data:OnetapgiftTag) -> None:

        self._checkUserRoomUserInRoom(data)

        if data.msg_id == 'sharedchatnotice':

            self.onetap_repo.save(Onetapgift(user_id=data.user_id,
                                            room_id=data.source_room_id,
                                            tmi_sent_ts=data.tmi_sent_ts,
                                            msg_id=data.msg_id,
                                            source_msg_id=data.source_msg_id,
                                            bits_spent=data.bits_spent,
                                            gift_id=data.gift_id,
                                            user_display_name=data.user_display_name,
                                            system_msg=data.system_msg))

        else:

            self.onetap_repo.save(Onetapgift(user_id=data.user_id,
                                            room_id=data.room_id,
                                            tmi_sent_ts=data.tmi_sent_ts,
                                            msg_id=data.msg_id,
                                            source_msg_id=data.source_msg_id,
                                            bits_spent=data.bits_spent,
                                            gift_id=data.gift_id,
                                            user_display_name=data.user_display_name,
                                            system_msg=data.system_msg))


    def _handlePaidupgrade(self, data:PaidupgradeTag) -> None:

        self._checkUserRoomUserInRoom(data)

        if data.msg_id == 'sharedchatnotice':

            self.paidupgrade_repo.save(Paidupgrade(user_id=data.user_id,
                                                   room_id=data.source_room_id,
                                                   tmi_sent_ts=data.tmi_sent_ts,
                                                   msg_id=data.msg_id,
                                                   source_msg_id=data.source_msg_id,
                                                   sender_login=data.sender_login,
                                                   sender_name=data.sender_name,
                                                   sub_plan=data.sub_plan,
                                                   system_msg=data.system_msg))

        else:

            self.paidupgrade_repo.save(Paidupgrade(user_id=data.user_id,
                                                   room_id=data.room_id,
                                                   tmi_sent_ts=data.tmi_sent_ts,
                                                   msg_id=data.msg_id,
                                                   source_msg_id=data.source_msg_id,
                                                   sender_login=data.sender_login,
                                                   sender_name=data.sender_name,
                                                   sub_plan=data.sub_plan,
                                                   system_msg=data.system_msg))

    def _handlePayforward(self, data:PayforwardTag) -> None:

        self._checkUserRoomUserInRoom(data)

        if data.msg_id == 'sharedchatnotice':

            self.payforward_repo.save(Payforward(user_id=data.user_id,
                                                 room_id=data.source_room_id,
                                                 tmi_sent_ts=data.tmi_sent_ts,
                                                 msg_id=data.msg_id,
                                                 source_msg_id=data.source_msg_id,
                                                 prior_gifter_anonymous=data.prior_gifter_anonymous,
                                                 prior_gifter_id=data.prior_gifter_id,
                                                 prior_gifter_display_name=data.prior_gifter_display_name,
                                                 prior_gifter_user_name=data.prior_gifter_user_name,
                                                 recipient_id=data.recipient_id,
                                                 recipient_display_name=data.recipient_display_name,
                                                 recipient_user_name=data.recipient_user_name,
                                                 system_msg=data.system_msg))

        else:

            self.payforward_repo.save(Payforward(user_id=data.user_id,
                                                 room_id=data.room_id,
                                                 tmi_sent_ts=data.tmi_sent_ts,
                                                 msg_id=data.msg_id,
                                                 source_msg_id=data.source_msg_id,
                                                 prior_gifter_anonymous=data.prior_gifter_anonymous,
                                                 prior_gifter_id=data.prior_gifter_id,
                                                 prior_gifter_display_name=data.prior_gifter_display_name,
                                                 prior_gifter_user_name=data.prior_gifter_user_name,
                                                 recipient_id=data.recipient_id,
                                                 recipient_display_name=data.recipient_display_name,
                                                 recipient_user_name=data.recipient_user_name,
                                                 system_msg=data.system_msg))

    def _handlePrivmsg(self, data:PrivmsgTag) -> None:

        self._checkUserRoomUserInRoom(data)

        self.privmsg_repo.save(Privmsg(tmi_sent_ts=data.tmi_sent_ts,
                                        message_id=data.message_id,
                                        source_message_id=data.souce_message_id,
                                        room_id=data.source_room_id,
                                        source_room_id=data.source_room_id,
                                        user_id=data.user_id,
                                        color=data.color,
                                        returning_chatter=data.returning_chatter,
                                        first_msg=data.first_msg,
                                        flags=data.flags,
                                        emotes=data.emotes,
                                        msg_content=data.msg_content))

    def _handleRaid(self, data:RaidTag) -> None:
        """Handles RAID messages"""

        self._checkUserRoomUserInRoom(data)
        # custom check for room and user

        self.raid_repo.save(Raid(user_id=data.user_id,
                                    room_id=data.source_room_id,
                                    tmi_sent_ts=data.tmi_sent_ts,
                                    msg_id=data.msg_id,
                                    source_msg_id=data.source_msg_id,
                                    msg_param_displayName=data.msg_param_displayName,
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
                                   cumulative_months=data.cumulative_months,
                                   months=data.months,
                                   multimonth_duration=data.multimonth_duration,
                                   multimonth_tenure=data.multimonth_tenure,
                                   should_share_streak=data.should_share_streak,
                                   sub_plan_name=data.sub_plan_name,
                                   sub_plan=data.sub_plan,
                                   was_gifted=data.was_gifted,
                                   system_msg=data.system_msg))
            
        else:
            
            self.sub_repo.save(Sub(user_id=data.user_id,
                                   room_id=data.source_room_id,
                                   tmi_sent_ts=data.tmi_sent_ts,
                                   msg_id=data.msg_id,
                                   source_msg_id=data.source_msg_id,
                                   cumulative_months=data.cumulative_months,
                                   months=data.months,
                                   multimonth_duration=data.multimonth_duration,
                                   multimonth_tenure=data.multimonth_tenure,
                                   should_share_streak=data.should_share_streak,
                                   sub_plan_name=data.sub_plan_name,
                                   sub_plan=data.sub_plan,
                                   was_gifted=data.was_gifted,
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
                                           community_gift_id=data.community_gift_id,
                                           fun_string=data.fun_string,
                                           gift_months=data.gift_months,
                                           months=data.months,
                                           origin_id=data.origin_id,
                                           recipient_id=data.recipient_id,
                                           recipient_display_name=data.recipient_display_name,
                                           recipient_user_name=data.recipient_user_name,
                                           sender_count=data.sender_count,
                                           sub_plan_name=data.sub_plan_name,
                                           sub_plan=data.sub_plan,
                                           system_msg=data.system_msg))

        else:

            self.subgift_repo.save(Subgift(user_id=data.user_id,
                                           room_id=data.room_id,
                                           tmi_sent_ts=data.tmi_sent_ts,
                                           msg_id=data.msg_id,
                                           source_msg_id=data.source_msg_id,
                                           community_gift_id=data.community_gift_id,
                                           fun_string=data.fun_string,
                                           gift_months=data.gift_months,
                                           months=data.months,
                                           origin_id=data.origin_id,
                                           recipient_id=data.recipient_id,
                                           recipient_display_name=data.recipient_display_name,
                                           recipient_user_name=data.recipient_user_name,
                                           sender_count=data.sender_count,
                                           sub_plan_name=data.sub_plan_name,
                                           sub_plan=data.sub_plan,
                                           system_msg=data.system_msg))

    def _handleSubmysterygift(self, data:SubmysteryTag) -> None:
        """Handles SUBMYSTERYGIFT messages"""

        self._checkUserRoomUserInRoom(data)

        if data.msg_id == 'sharedchatnotice':

            self.subgift_repo.save(Submystery(user_id=data.user_id,
                                              room_id=data.source_room_id,
                                              tmi_sent_ts=data.tmi_sent_ts,
                                              msg_id=data.msg_id,
                                              source_msg_id=data.souce_msg_id,
                                              community_gift_id=data.community_gift_id,
                                              contribution_type=data.contribution_type,
                                              current_contributions=data.current_contributions,
                                              target_contributions=data.target_contributions,
                                              user_contributions=data.user_contributions,
                                              mass_gift_count=data.mass_gift_count,
                                              origin_id=data.origin_id,
                                              sub_plan=data.sub_plan,
                                              system_msg=data.system_msg))

        else:

            self.subgift_repo.save(Submystery(user_id=data.user_id,
                                              room_id=data.room_id,
                                              tmi_sent_ts=data.tmi_sent_ts,
                                              msg_id=data.msg_id,
                                              source_msg_id=data.souce_msg_id,
                                              community_gift_id=data.community_gift_id,
                                              contribution_type=data.contribution_type,
                                              current_contributions=data.current_contributions,
                                              target_contributions=data.target_contributions,
                                              user_contributions=data.user_contributions,
                                              mass_gift_count=data.mass_gift_count,
                                              origin_id=data.origin_id,
                                              sub_plan=data.sub_plan,
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
                                                           streak=data.param_value))
            
        else:
            self.viewerMilestone_repo.save(ViewerMilestone(room_id=data.room_id,
                                                           user_id=data.user_id,
                                                           display_name=data.display_name,
                                                           streak=data.param_value))


# Helpers

    def _checkUserRoomUserInRoom(self, data:BaseTag) -> None:

        if data.msg_id == 'sharedchatnotice':

            # extract substreak
            if data.get('badges') != '':
                badges = data.get('badges').split(',')
                for badge in badges:
                    if badge.startswith('subscriber'):
                        data.sub_substreak = int(badge.split('/')[1])

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
                                         room_name=data.room_name))

            # check whether user exists in user_in_room table
            if not self.userRoom_repo.exists(room_id=data.source_room_id, user_id=data.user_id):

                self.userRoom_repo.save(UserRoom(user_id=data.user_id,
                                                 room_id=data.source_room_id,
                                                 badges=data.source_badges,
                                                 badge_info=data.source_badge_info,
                                                 sub=data.sub,
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
                                                 sub=data.sub,
                                                 sub_streak=data.sub_streak,
                                                 vip=data.vip,
                                                 mod=data.mod))