from ..repositories import (UserRepository, 
                            RoomRepository, 
                            MessageRepository, 
                            UserInRoomRepository, 
                            SubRepository)

class SaltmineService:

    def __init__(self,
                 user_repo: UserRepository,
                 room_repo: RoomRepository,
                 message_repo: MessageRepository,
                 userInRoom_repo: UserInRoomRepository,
                 sub_repo: SubRepository):
        
        self.user_repo = user_repo
        self.room_repo = room_repo
        self.message_repo = message_repo
        self.userInRoom_repo = userInRoom_repo
        self.sub_repo = sub_repo

    def process_message(self, parsed_message: dict) -> None:
        """Process parsed message"""
        pass