from models import MessageInRoom, Sub, Subgift, UserInRoom
from db.repositories.base import Saltminer as sm


class Saltshaker:

    def parse_privmsg(self, message:str) -> None:
        """Parse tags into dictionary"""

        try:
            # we build a separator ' :{display-name}' to separate tags and message
            start = message.find('display-name=')
            if start == -1:
                raise ValueError("PRIVMSG message is corrupted: no 'display-name'")
            
            start +=  len('display-name=')
            end = message.find(';', start)
            if end == -1:
                raise ValueError("PRIVMSG message is corrupted: no ';' after display-name")
            
            separator = f' :{message[start:end]}'

            # find the end of tags
            boundary = message.find(separator)
            if boundary == -1:
                raise ValueError("PRIVMSG message is corrupted: cannot separate tags from message part")

            parsed = {}
            tags = message[1:boundary]
            for tag in tags.split(';'):
                if '=' in tag:
                    key, value = tag.split('=', 1)
                    parsed[key] = value if value else None
            
            # parse message
            message = message[boundary+2:]  # skip first ' :'
            
            idx = message.find('#')
            if idx == -1:
                raise ValueError("PRIVMSG message is corrupted: no '#' in message part")
            room_name = message[idx+1:message.find(' ', idx)].strip()

            idx = message.find(' :')
            if idx == -1:
                raise ValueError("PRIVMSG message is corrupted: no ' :' in message part")

            # add to message in channel table

            # check whether user is present in user table
            if not sm._check_user(parsed.get('user-id')):
                sm.upsert_user(user_id=parsed.get('user-id'),
                               display_name=parsed.get('display-name'),
                               username=parsed.get('display-name').lower(),
                               color=parsed.get('color'),
                               turbo=int(parsed.get('turbo', '0')))
            
            # check whether room/source-room is present in room table             
            if ('source-room-id' in parsed and 
                not sm._check_room(parsed.get('source-room-id'))):
                
                sm.upsert_room(room_id=parsed.get('source-room-id'),
                               room_name='unknown')
                
            if not sm._check_room(parsed.get('room-id')):

                sm.upsert_room(room_id=parsed.get('room-id'),
                               room_name=room_name)

            # upsert user in user_in_room table
            user_room = UserInRoom(user_id=parsed.get('user-id'),
                                   returning_chatter=int(parsed.get('returning-chatter')),
                                   first_message=int(parsed.get('first-message')),
                                   sub=int(parsed.get('subscriber')),
                                   badges=parsed.get('badges'),
                                   user_type=parsed.get('user-type'))
            
            if 'source-room-id' in parsed:
                user_room.room_id=parsed.get('source-room-id')
            else:
                user_room.room_id=parsed.get('room-id')

            if sm._check_user_in_room(room_id=user_room.room_id):

                if parsed.get('source-badge') is 'vip':
                    user_room.vip=1
                elif parsed.get('mod') is '1':
                    user_room.mod=1
                            
                sm.upsert_user_in_room(room_id=user_room.room_id,
                                       user_id=user_room.user_id,
                                       returning_chatter=user_room.returning_chatter,
                                       first_message=user_room.first_message,
                                       sub=user_room.sub,
                                       vip=user_room.vip,
                                       mod=user_room.mod,
                                       badges=user_room.badges,
                                       user_type=user_room.user_type)

            # add message to message_in_room
            message = MessageInRoom(message_id=parsed.get('id'),
                                    user_id=parsed.get('user-id'))
            if 'source-room-id' in parsed:
                message(room_id=parsed.get('source-room-id'))
            else:
                message(room_id=parsed.get('room-id'))
            if 'reply-parent-msg-id' in parsed:
                message(reply_message_id=parsed.get('reply-parent-msg-id'))
                message(reply_user_id=parsed.get('reply-parent-user-id'))
                message(reply_display_name=parsed.get('reply-parent-display-name'))
            if 'reply-thread-parent-msg-id' in parsed:
                message(thread_message_id=parsed.get('reply-thread-parent-msg-id'))
                message(thread_user_id=parsed.get('reply-thread-parent-user-id'))
                message(thread_display_name=parsed.get('reply-thread-parent-display-name'))

            sm.insert_message_in_room(message.message_id,
                                      message.user_id,
                                      message.room_id,
                                      message.reply_message_id,
                                      message.reply_user_id,
                                      message.reply_display_name,
                                      message.thread_message_id,
                                      message.thread_user_id,
                                      message.thread_display_name)

        except Exception as e:
            print(f'Error parsing PRIVMSG: {e}')

    def parse_usernotice(self, message:str) -> None:
        """Parse USERNOTICE messages"""

        try:
            tags_end = message.find(' :tmi.twitch.tv')
            if tags_end == -1:
                raise ValueError("USERNOTICE message is corrupted: no ' :'")

            idx = message[tags_end:].find(' #')
            if idx == -1:
                raise ValueError("USERNOTICE message is corrupted: no '#'")
            
            room_name = message[idx+1:].strip()
            tags = message[1:tags_end]
            tags_parsed = {}
            for tag in tags.split(';'):
                if '=' in tag:
                    key, value = tag.split('=',1)
                    tags_parsed[key] = value if value else None
            
            if tags_parsed == {}:
                raise ValueError("USERNOTICE message is corrupted: no tags")
            
            # check whether user is present in user table
            if not sm._check_user(tags_parsed.get('user-id')):
                sm.upsert_user(user_id=tags_parsed.get('user-id'),
                               display_name=tags_parsed.get('display-name'),
                               username=tags_parsed.get('display-name').lower(),
                               color=tags_parsed.get('color'),
                               turbo=int(tags_parsed.get('turbo', '0')))

            # check whether room is present
            if ('msg-id' == 'sharedchatnotice' and 
                not sm._check_room(tags_parsed.get('source-room-id'))):
            
                sm.upsert_room(room_id=tags_parsed.get('source-room-id'),
                               room_name='unknown')
            
            if not sm._check_room(tags_parsed.get('room-id')):

                sm.upsert_room(room_id=tags_parsed.get('room-id'),
                               room_name=room_name)

            # upsert user in user_in_room table
            user_room = UserInRoom(user_id=tags_parsed.get('user-id'),
                                   sub=int(tags_parsed.get('subscriber')),
                                   badges=tags_parsed.get('badges'),
                                   user_type=tags_parsed.get('user-type'))
            
            if 'msg-id' == 'sharedchatnotice':
                user_room.room_id=tags_parsed.get('source-room-id')
            else:
                user_room.room_id=tags_parsed.get('room-id')

            if sm._check_user_in_room(room_id=user_room.room_id):

                if tags_parsed.get('vip') is '1':
                    user_room.vip=1
                elif tags_parsed.get('mod') is '1':
                    user_room.mod=1
                            
                sm.upsert_user_in_room(room_id=user_room.room_id,
                                       user_id=user_room.user_id,
                                       returning_chatter=user_room.returning_chatter,
                                       first_message=user_room.first_message,
                                       sub=user_room.sub,
                                       vip=user_room.vip,
                                       mod=user_room.mod,
                                       badges=user_room.badges,
                                       user_type=user_room.user_type)

            # sub, resub
            if (tags_parsed.get('msg-id') in ['sub', 'resub'] or 
                tags_parsed.get('source-msg-id') in ['sub', 'resub']):
            
                # sub, resub
                sub = Sub(user_id=tags_parsed.get('user-id'),
                          sub_plan=tags_parsed.get('msg-param-sub-plan'),
                          months=int(tags_parsed.get('msg-param-months')),
                          multimonth_duration=int(tags_parsed.get('msg-param-multimonth-duration')),
                          multimonth_tenure=int(tags_parsed.get('msg-param-multimonth-tenure')),
                          streak_months=0,
                          share_streak=int(tags_parsed.get('msg-param-should-share-streak')),
                          cumulative=int(tags_parsed.get('msg-param-cumulative-months')))
                if tags_parsed.get('msg-id') == 'sharedchatnotice':
                    sub.room_id=tags_parsed.get('source-room-id')
                    sub.message_id=tags_parsed.get('source-id')
                else:
                    sub.room_id=tags_parsed.get('room-id')
                    sub.message_id=tags_parsed.get('id')

                #if tags_parsed.get('msg-param-was-gifted') == 'true':
                #    Sub.gift_id=tags_parsed.get('???')
                #    Sub.gift_months=int(tags_parsed.get('???'))
                
                #placeholder for gift_id and gift_months
                sub.gift_id=''
                sub.gift_months=0

                sm.insert_subs(user_id=sub.user_id,
                               room_id=sub.room_id,
                               message_id=sub.message_id,
                               gift_id=sub.gift_id,
                               sub_plan=sub.sub_plan,
                               months=sub.months,
                               gift_months=sub.gift_months,
                               multimonth_duration=sub.multimonth_duration,
                               multimonth_tenure=sub.multimonth_tenure,
                               streak_months=sub.streak_months,
                               share_streak=sub.share_streak,
                               cumulative=sub.cumulative)

            # subgift, submysterygift 
            if (tags_parsed.get('msg-id') in ['subgift', 'submysterygift'] or 
                tags_parsed.get('source-msg-id') in ['subgift', 'submysterygift']):
            
                if (tags_parsed.get('msg-id') == 'subgift' or 
                    tags_parsed.get('source-msg-id') == 'subgift'):
                
                    gift = Subgift(user_id=tags_parsed.get('user-id'),
                                   gift_id=tags_parsed.get('msg-param-community-gif-id'),
                                   gift_count=0,
                                   gifter_total=tags_parsed.get('msg-param-sender-count'),
                                   sub_plan=tags_parsed.get('msg-param-sub-plan'))

                    sub = Sub(user_id=tags_parsed.get('msg-param-recipient-id'),
                              room_id=gift.room_id,
                              gift_id=tags_parsed.get('msg-param-community-gift-id'),
                              sub_plan=tags_parsed.get('msg-param-sub-plan'),
                              months=tags_parsed.get('msg-param-months'),
                              gift_months=tags_parsed.get('msg-param-gift-months'),
                              multimonth_duration=0,
                              multimonth_tenure=0,
                              streak_months=0,
                              share_streak=0,
                              cumulative=0)

                    if tags_parsed.get('msg-id') == 'sharedchatnotice':
                        gift.room_id=tags_parsed.get('sourceroom-id')
                        sub.message_id=tags_parsed.get('source-id')
                    else:
                        gift.room_id=tags_parsed.get('room-id')
                        sub.message_id=tags_parsed.get('id')

                    sm.insert_subgift(user_id=gift.user_id,
                                      room_id=gift.room_id,
                                      gift_id=gift.gift_id,
                                      gift_count=gift.gift_count,
                                      gifter_total=gift.gifter_total,
                                      sub_plan=gift.sub_plan)
                    
                    sm.insert_subs(user_id=sub.user_id,
                                   room_id=sub.room_id,
                                   message_id=sub.message_id,
                                   gift_id=sub.gift_id,
                                   sub_plan=sub.sub_plan,
                                   months=sub.months,
                                   gift_months=sub.gift_months,
                                   multimonth_duration=sub.multimonth_duration,
                                   multimonth_tenure=sub.multimonth_tenure,
                                   streak_months=sub.streak_months,
                                   share_streak=sub.share_streak,
                                   cumulative=sub.cumulative)
                
                else:
                    gift = Subgift(user_id=tags_parsed.get('user-id'),
                                   gift_id=tags_parsed.get('msg-param-community-gif-id'),
                                   gift_count=int(tags_parsed.get('msg-param-mass-gift-count')),
                                   gifter_total=int(tags_parsed.get('msg-param-sender-count')),
                                   sub_plan=tags_parsed.get('msg-param-sub-plan'))

                    if tags_parsed.get('msg-id') == 'sharedchatnotice':
                        gift.room_id=tags_parsed.get('source-room-id')
                    else:
                        gift.room_id=tags_parsed.get('room-id')

                    sm.insert_subgift(user_id=gift.user_id,
                                      room_id=gift.room_id,
                                      gift_id=gift.gift_id,
                                      gift_count=gift.gift_count,
                                      gifter_total=gift.gifter_total,
                                      sub_plan=gift.sub_plan)
     
            # watch-streak - not implemented yet
                
        except Exception as e:
            print(f'Error parsing USERNOTICE: {e}')
        
    def parse_join(self, message:str) -> None:
        """Parse channel JOIN message"""

        try:
            idx = message.find('!')
            if idx == -1:
                raise ValueError("JOIN message is corrupted: no '!'")

            display_name = message[1:idx]

            idx = message.find('JOIN #')
            if idx == -1:
                raise ValueError("JOIN messaee is corrupted: no '#'")

            room_name = message[idx+1:].strip()

            # Add upsert into userlist
            sm.insert_userlist(room_name=room_name,
                               display_name=display_name,
                               join_part='JOIN')

        except Exception as e:
            print(f'Error parsing JOIN: {e}')


    def parse_part(self, message:str) -> None:
        """Parse channel PART message"""

        try:
            idx = message.find('!')
            if idx == -1:
                raise ValueError("PART message is corrupted: no '!'")
            
            display_name = message[1:idx]

            idx = message.find('PART #')
            if idx == -1:
                raise ValueError("PART message is corrupted: no '#'")
            
            room_name = message[idx+1:].strip()

            # Add upsert into userlist

            sm.insert_userlist(room_name=room_name,
                               display_name=display_name,
                               join_part='PART')

        except Exception as e:
            print(f'Error parsing PART: {e}')

    def parse(self, line:str) -> None:
        """Parse IRC line into dictionary"""

        if ' PRIVMSG ' in line:
            self.parse_privmsg(line)

        if ' USERNOTICE ' in line:
            self.parse_usernotice(line)

        if ' JOIN ' in line:
            self.parse_join(line)
    
        if ' PART ' in line:
            self.parse_part(line)