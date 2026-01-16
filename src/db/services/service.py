
from ..repositories import (AnnouncementRepository,
                            BitsRepository, 
                            MessageRepository,
                            RaidRepository,
                            RoomRepository,
                            RoomStateRepository,
                            SubRepository,
                            SubgiftRepository,
                            UserRepository,  
                            UserInRoomRepository,
                            UserlistRepository,
                            ViewerMilestoneRepository)
from ..models import (Announcement,
                      User, 
                      Room,
                      Roomstate, 
                      UserInRoom, 
                      MessageInRoom, 
                      Sub, 
                      Subgift, 
                      UserListEntry,
                      ViewerMilestone)

from parsers.tags import (AnnouncementTag, 
                          BaseTag, 
                          PrivmsgTag, 
                          RoomstateTag, 
                          SubgiftTag, 
                          SubmysterygiftTag,
                          SubTag, 
                          ViewerMilestoneTag)

from dataclasses import fields

MISSING_NUM = -1
MISSING_STR = 'null'

class SaltyService:

    def __init__(self,
                 announcement_repo: AnnouncementRepository,
                 bits_repo: BitsRepository,
                 message_repo: MessageRepository,
                 raid_repo: RaidRepository,
                 room_repo: RoomRepository,
                 roomstate_repo: RoomStateRepository,
                 sub_repo: SubRepository,
                 subgift_repo: SubgiftRepository,
                 user_repo: UserRepository,
                 userInRoom_repo: UserInRoomRepository,
                 userlist_repo: UserlistRepository,
                 viewerMilestone_repo: ViewerMilestoneRepository):
        
        self.announcement_repo = announcement_repo
        self.bits_repo = bits_repo
        self.message_repo = message_repo
        self.raid_repo = raid_repo
        self.room_repo = room_repo
        self.roomstate_repo = roomstate_repo
        self.sub_repo = sub_repo
        self.subgift_repo = subgift_repo
        self.user_repo = user_repo
        self.userInRoom_repo = userInRoom_repo
        self.userlist_repo = userlist_repo
        self.viewerMilestone_repo = viewerMilestone_repo

    def process_message(self, parsed: dict) -> None:
        """Process parsed message"""

        if not parsed.is_valid:
            print(f'PROCESS MESSAGE: Corrupted message: {parsed.error} (Variable: {parsed})')
            return
        
        if parsed.message_type == 'PRIVMSG':
            self._handlePrivMessage(parsed.data)
        elif parsed.message_type == 'SUBSCRIPTION':
            self._handleSubscription(parsed.data)
        elif parsed.message_type == 'SUBGIFT':
            self._handleSubgift(parsed.data)
        elif parsed.message_type == 'SUBMYSTERYGIFT':
            self._handleSubmysterygift(parsed.data)
        elif parsed.message_type == 'ROOMSTATE':
            self._handleRoomstate(parsed.data)
        elif parsed.message_type == 'ANNOUNCEMENT':
            self._handleAnnouncement(parsed.data)
        elif parsed.message_type == 'VIEWERMILESTONE':
            self._handleViewerMilestone(parsed.data)
        elif parsed.message_type == 'JOIN':
            self._handleJoin(parsed.data)
        elif parsed.message_type == 'PART':
            self._handlePart(parsed.data)

    def _handlePrivMessage(self, data:PrivmsgTag) -> None:
        """Handles PRIVMSG messages"""

        if data.msg_id == 'sharedchatnotice':
  
            self._checkUserRoomUserInRoom(data)

            # add message to message_in_room table
            self.message_repo.save(MessageInRoom(message_id=data.id,
                                                 room_id=data.source_room_id,
                                                 user_id=data.user_id,
                                                 reply_message_id=data.reply_parent_msg_id,
                                                 reply_user_id=data.reply_parent_user_id,
                                                 reply_display_name=data.reply_parent_display_name,
                                                 thread_message_id=data.reply_thread_parent_msg_id,
                                                 thread_user_id=data.reply_thread_parent_user_id,
                                                 thread_display_name=data.reply_thread_parent_display_name,
                                                 content=data.message_content))

        else:

            self._checkUserRoomUserInRoom(data)

            # add message to message_in_room table
            self.message_repo.save(MessageInRoom(message_id=data.id,
                                                 room_id=data.room_id,
                                                 user_id=data.user_id,
                                                 reply_message_id=data.reply_parent_msg_id,
                                                 reply_user_id=data.reply_parent_user_id,
                                                 reply_display_name=data.reply_parent_display_name,
                                                 thread_message_id=data.reply_thread_parent_msg_id,
                                                 thread_user_id=data.reply_thread_parent_user_id,
                                                 thread_display_name=data.reply_thread_parent_display_name,
                                                 content=data.message_content))

    def _handleSubscription(self, data:SubTag) -> None:
        """Handles SUB messages"""

        self._checkUserRoomUserInRoom(data)

        if data.msg_id == 'sharedchatnotice':
    
            self.sub_repo.save(Sub(user_id=data.user_id,
                                   room_id=data.source_room_id,
                                   message_id=data.id,
                                   gift_id=MISSING_STR,
                                   sub_plan=data.sub_plan,
                                   months=int(data.months),
                                   gift_months=MISSING_NUM,
                                   multimonth_duration=int(data.multimonth_duration),
                                   multimonth_tenure=int(data.multimonth_tenure),
                                   streak_months=MISSING_NUM,
                                   share_streak=int(data.should_share_streak),
                                   cumulative=int(data.cumulative_months)))
            
        else:
            
            self.sub_repo.save(Sub(user_id=data.user_id,
                                   room_id=data.room_id,
                                   message_id=data.id,
                                   gift_id=MISSING_STR,
                                   sub_plan=data.sub_plan,
                                   months=int(data.months),
                                   gift_months=MISSING_NUM,
                                   multimonth_duration=int(data.multimonth_duration),
                                   multimonth_tenure=int(data.multimonth_tenure),
                                   streak_months=MISSING_NUM,
                                   share_streak=int(data.should_share_streak),
                                   cumulative=int(data.cumulative_months)))


    def _handleSubgift(self, data:SubgiftTag) -> None:
        """Handles SUBGIFT messages"""

        self._checkUserRoomUserInRoom(data)

        if data.msg_id == 'sharedchatnotice':

            self.subgift_repo.save(Subgift(user_id=data.user_id,
                                           room_id=data.source_room_id,
                                           gift_id=data.gift_id,
                                           gift_count=MISSING_NUM,
                                           gifter_total=int(data.sender_count),
                                           sub_plan=data.sub_plan))

        else:

            self.subgift_repo.save(Subgift(user_id=data.user_id,
                                           room_id=data.room_id,
                                           gift_id=data.gift_id,
                                           gift_count=MISSING_NUM,
                                           gifter_total=int(data.sender_count),
                                           sub_plan=data.sub_plan))

    def _handleSubmysterygift(self, data:SubmysterygiftTag) -> None:
        """Handles SAUBMYSTERYGIFT messages"""

        self._checkUserRoomUserInRoom(data)

        if data.msg_id == 'sharedchatnotice':

            self.subgift_repo.save(Subgift(user_id=data.user_id,
                                           room_id=data.source_room_id,
                                           gift_id=data.gift_id,
                                           gift_count=int(data.mass_gift_count),
                                           gifter_total=int(data.sender_count),
                                           sub_plan=data.sub_plan))

        else:

            self.subgift_repo.save(Subgift(user_id=data.user_id,
                                           room_id=data.room_id,
                                           gift_id=data.gift_id,
                                           gift_count=int(data.mass_gift_count),
                                           gifter_total=int(data.sender_count),
                                           sub_plan=data.sub_plan))

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
                                           followers_only=int(data.followers_only),
                                           sub_only=int(data.sub_only),
                                           emote_only=int(data.emote_only),
                                           slow_mode=int(data.slow_mode),
                                           r9k=int(data.r9k)))

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


    def _handleJoin(self, data:dict) -> None:
        """Handles JOIN messages"""

        self.userlist_repo.save(UserListEntry(room_name=data.get('room-name'),
                                              display_name=data.get('display-name'),
                                              join_part=data.get('msg-type')))

    def _handlePart(self, data:dict) -> None:
        """Handles PART messages"""

        self.userlist_repo.save(UserListEntry(room_name=data.get('room-name'),
                                              display_name=data.get('display-name'),
                                              join_part=data.get('msg-type')))

# Helpers

    def _checkUserRoomUserInRoom(self, data:BaseTag) -> None:

        if data.msg_id == 'sharedchatnotice':


            if not self.user_repo.exists(user_id=data.user_id):
            
                # check whether user exists in user table
                self.user_repo.save(User(user_id=data.user_id,
                                        display_name=data.display_name,
                                        username=data.username,
                                        color=data.color,
                                        turbo=int(data.turbo)))

            # check whether room and source-room exist in room table
            if not self.room_repo.exists(room_id=data.source_room_id):

                self.room_repo.save(Room(room_id=data.source_room_id,
                                        room_name=data.room_name))

            # check whether user exists in user_in_room table
            if not self.userInRoom_repo.exists(room_id=data.source_room_id, user_id=data.user_id):

                self.userInRoom_repo.save(UserInRoom(room_id=data.source_room_id,
                                                     user_id=data.user_id,
                                                     returning_chatter=int(data.returning_chatter),
                                                     first_message=int(data.first_msg),
                                                     sub=int(data.sub),
                                                     vip=int(data.vip),
                                                     mod=int(data.mod),
                                                     badges=data.source_badges,
                                                     user_type=data.user_type))
        
        else:

            # check whether user exists in user table
            if not self.user_repo.exists(user_id=data.user_id):
                
                self.user_repo.save(User(user_id=data.user_id,
                                         display_name=data.display_name,
                                         username=data.username,
                                         color=data.color,
                                         turbo=int(data.turbo)))

            # check whether room and source-room exist in room table
            if not self.room_repo.exists(room_id=data.room_id):

                self.room_repo.save(Room(room_id=data.room_id,
                                         room_name=data.room_name))


            # check whether user exists in user_in_room table
            if not self.userInRoom_repo.exists(room_id=data.room_id, user_id=data.user_id):
                
                self.userInRoom_repo.save(UserInRoom(room_id=data.room_id,
                                                     user_id=data.user_id,
                                                     returning_chatter=int(data.returning_chatter),
                                                     first_message=int(data.first_msg),
                                                     sub=int(data.sub),
                                                     vip=int(data.vip),
                                                     mod=int(data.mod),
                                                     badges=data.badges,
                                                     user_type=data.user_type))