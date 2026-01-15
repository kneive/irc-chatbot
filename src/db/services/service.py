from ..repositories import (BitsRepository, 
                            MessageRepository,
                            RaidRepository,
                            RoomRepository,
                            RoomStateRepository,
                            SubRepository,
                            SubgiftRepository,
                            UserRepository,  
                            UserInRoomRepository,
                            UserlistRepository 
                            )
from ..models import (User, 
                      Room, 
                      UserInRoom, 
                      MessageInRoom, 
                      Sub, 
                      Subgift, 
                      UserListEntry)

class SaltyService:

    def __init__(self,
                 bits_repo: BitsRepository,
                 message_repo: MessageRepository,
                 raid_repo: RaidRepository,
                 room_repo: RoomRepository,
                 roomstate_repo: RoomStateRepository,
                 sub_repo: SubRepository,
                 subgift_repo: SubgiftRepository,
                 user_repo: UserRepository,
                 userInRoom_repo: UserInRoomRepository,
                 userlist_repo: UserlistRepository):
        
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

    def process_message(self, parsed: dict) -> None:
        """Process parsed message"""

        if not parsed.is_valid:
            print(f'PROCESS MESSAGE: Corrupted message: {parsed.error} (Variable: {parsed})')
            return
        
        if parsed.message_type == 'PRIVMSG':
            self._handlePrivMessage(parsed.data)
        elif parsed.message_type == 'USERNOTICE':
            self._handleUserNotice(parsed.data)
        elif parsed.message_type == 'ROOMSTATE':
            pass
        elif parsed.message_type == 'JOIN':
            self._handleJoin(parsed.data)
        elif parsed.message_type == 'PART':
            self._handlePart(parsed.data)

    def _handlePrivMessage(self, data:dict) -> None:
        """Handles PRIVMSG messages"""

        # check whether user exists in user table
        if not self.user_repo.exists(user_id=data.get('user-id')):
            
            self.user_repo.save(User(user_id=data.get('user-id'),
                                     display_name=data.get('display-name'),
                                     username=data.get('username'),
                                     color=data.get('color'),
                                     turbo=int(data.get('turbo'))))

        # check whether room exists in room table
        if not self.room_repo.exists(room_id=data.get('room-id')):

            self.room_repo.save(Room(room_id=data.get('room-id'),
                                     room_name=data.get('room-name')))

        # check whether user exists in user_in_room table
        if not self.userInRoom_repo.exists(room_id=data.get('room-id'),
                                           user_id=data.get('user-id')):
            
            self.userInRoom_repo.save(UserInRoom(room_id=data.get('room-id'),
                                                 user_id=data.get('user-id'),
                                                 returning_chatter=int(data.get('returning-chatter')),
                                                 first_message=int(data.get('first-msg')),
                                                 sub=int(data.get('sub')),
                                                 vip=int(data.get('vip')),
                                                 mod=int(data.get('mod')),
                                                 badges=data.get('badges'),
                                                 user_type=data.get('user-type')))

        # add message to message_in_room table
        self.message_repo.save(MessageInRoom(message_id=data.get(msg-id),
                                             room_id=data.get('room-id'),
                                             user_id=data.get('user-id'),
                                             reply_message_id=data.get('reply-msg-id'),
                                             reply_user_id=data.get('reply-user-id'),
                                             reply_display_name=data.get('reply-display-name'),
                                             thread_message=data.get('thread-msg-id'),
                                             thread_user_id=data.get('thread-user-id'),
                                             thread_display_name=data.get('thread-display-name'),
                                             content=data.get('message-content')))

    def _handleUserNotice(self, data:dict) -> None:
        """Handles USERNOTICE messages"""

        # check whether user exists in user table
        if not self.user_repo.exists(user_id=data.get('user-id')):
            
            self.user_repo.save(User(user_id=data.get('user-id'),
                                     display_name=data.get('display-name'),
                                     username=data.get('username'),
                                     color=data.get('color'),
                                     turbo=int(data.get('turbo'))))

        # check whether room exists in room table
        if not self.room_repo.exists(room_id=data.get('room-id')):

            self.room_repo.save(Room(room_id=data.get('room-id'),
                                     room_name=data.get('room-name')))

        # check whether user exists in user_in_room table
        if not self.userInRoom_repo.exists(room_id=data.get('room-id'),
                                           user_id=data.get('user-id')):
            
            self.userInRoom_repo.save(UserInRoom(room_id=data.get('room-id'),
                                                 user_id=data.get('user-id'),
                                                 returning_chatter=int(data.get('returning-chatter')),
                                                 first_message=int(data.get('first-msg')),
                                                 sub=int(data.get('sub')),
                                                 vip=int(data.get('vip')),
                                                 mod=int(data.get('mod')),
                                                 badges=data.get('badges'),
                                                 user_type=data.get('user-type')))

        # add sub
        if data.get('msg-id') in ['subgift', 'submysterygift']:
            self.subgift_repo.save(Subgift(user_id=data.get('user-id'),
                                           room_id=data.get('room-id'),
                                           gift_id=data.get('gift-id'),
                                           gift_count=int(data.get('gift-count')),
                                           gifter_total=int(data.get('gifter-total')),
                                           sub_plan=data.get('sub-plan')))
        
        elif data.get('msg-id') in ['sub', 'resub', 'subgift']:
            self.sub_repo.save(Sub(user_id=data.get('user-id'),
                                    room_id=data.get('room-id'),
                                    message_id=data.get('msg-id'),
                                    gift_id=data.get('gift-id', '-1'),
                                    sub_plan=data.get('sub-plan'),
                                    months=int(data.get('months')),
                                    gift_months=int(data.get('gift-months', '-1')),
                                    multimonth_duration=int(data.get('multimonth-duration')),
                                    multimonth_tenure=int(data.get('multimonth-tenure')),
                                    streak_months=int(data.get('streak-months', '-1')),
                                    share_streak=int(data.get('share-streak')),
                                    cumulative=int(data.get('cumulative'))))

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