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

class SaltmineService:

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

    def process_message(self, parsed_message: dict) -> None:
        """Process parsed message"""
        pass