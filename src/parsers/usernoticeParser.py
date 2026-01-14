from .base import BaseParser, ParseResult
from typing import Optional, Dict

class UsernoticeParser(BaseParser):

    def parseable(self, input:str) -> bool:
        """Check whether the input is parseable by this parser"""

        return ' USERNOTICE ' in input
    
    def parse(self, input:str) -> Optional[ParseResult]:
        """Parse input and return ParseResult or None"""

        try:
            end = input.find(' :tmi.twitch.tv')
            if end == -1:
                raise ValueError("USERNOTICE message is corrupted: no ' :'")

            raw_tags = self._parseTags(input[1:end])

            idx = input[end:].find(' #')
            if idx == -1:
                raise ValueError("USERNOTICE message is corrupted: no '#'")
            
            room = input[idx+1:].strip()

            tags = {}

            if (raw_tags.get('msg-id') in ['sub', 'resub'] or 
                raw_tags.get('source-msg-id') in ['sub', 'resub']):

                tags = self._parseSub(raw_tags, room)

            elif (raw_tags.get('msg-id') is 'submysterygift' or 
                  raw_tags.get('source-msg-id') is 'submysterygift'):

                tags = self._parseSubmysterygift(raw_tags, room)

            elif (raw_tags.get('msg-id') is 'subgift' or 
                  raw_tags.get('source-msg-id') is 'subgift'):
            
                tags =self._parseSubgift(raw_tags, room)

            return ParseResult('USERNOTICE',
                               tags,
                               input)


        except Exception as e:
            print(f'USERNOTICE is corrupted')
            result = ParseResult('USERNOTICE', {}, input)
            result.is_valid = False
            result.error = str(e)
            return result

    def _parseTags(self, input:str) -> Dict[str, str]:
        """Parse message tags from input string"""

        try:
            tags = {}
            for tag in input.split(';'):
                if '=' in tag:
                    key, value = tag.split('=', 1)
                    tags[key] = value if value else None
            
            return tags

        except ValueError as e:
            raise ValueError('PRIVMSG message is corrupted')
        
    def _parseSub(self, raw_tags:Dict[str,str], room:str) -> Dict[str,str]:
        """Parse sub / resub specific tags"""

        tags = {}

        if 'source-room-id' in raw_tags:
            tags['room-id'] = raw_tags.get('source-room-id')
            tags['room-name'] = '#unknown'
        else:
            tags['room-id'] = raw_tags.get('room-id')
            tags['room-name'] = room
        
        tags['user-id'] = raw_tags.get('user-id')
        tags['display-name'] = raw_tags.get('display-name')
        tags['username'] = raw_tags.get('display-name').lower()
        
        tags['color'] = raw_tags.get('color')
        tags['badges'] = raw_tags.get('badges')
        
        tags['turbo'] = '-1'
        
        tags['sub'] = raw_tags.get('subscriber', '0')
        tags['vip'] = raw_tags.get('vip', '0')
        tags['mod'] = raw_tags.get('mod', '0')
        tags['user-type'] = raw_tags.get('user-type')

        tags['first-message'] = '0'
        tags['returning-chatter'] = '0'

        tags['sub-plan'] = raw_tags.get('msg-param-sub-plan')
        tags['months'] = raw_tags.get('msg-param-months')
        tags['multimonth-duration'] = raw_tags.get('msg-param-multimonth-duration')
        tags['multimonth-tenure'] = raw_tags.get('msg-param-multimonth-tenure')
        tags['streak-months'] = '-1'
        tags['share-streak'] = raw_tags.get('msg-param-should-share-streak')
        tags['cumulative'] = raw_tags.get('msg-param-cumulative-months')
        tags['msg-id'] = raw_tags.get('source-msg-id', raw_tags.get('msg-id'))

        return tags


    def _parseSubgift(self, raw_tags:Dict[str,str], room:str) -> Dict[str,str]:
        """Parse subgift specific tags"""

        tags = {}

        if 'source-room-id' in raw_tags:
            tags['room-id'] = raw_tags.get('source-room-id')
            tags['room-name'] = '#unknown'
        else:
            tags['room-id'] = raw_tags.get('room-id')
            tags['room-name'] = room

        tags['user-id'] = raw_tags.get('msg-param-recipient-id')
        tags['display-name'] = raw_tags.get('msg-param-recipient-display-name')
        tags['username'] = raw_tags.get('msg-param-recipient-display-name').lower()
        
        tags['color'] = raw_tags.get('color')
        tags['badges'] = 'null'
        tags['badge-info'] = 'null'
        
        tags['turbo'] = '-1'
        
        tags['sub'] = raw_tags.get('subscriber', '0')
        tags['vip'] = raw_tags.get('vip', '0')
        tags['mod'] = raw_tags.get('mod', '0')
        tags['user-type'] = raw_tags.get('user-type')

        tags['gift-id'] = raw_tags.get('msg-param-community-gift-id', 'null')
        tags['gift-count'] = raw_tags.get('msg-param-sender-count', '-1')
        tags['gifter-total'] = raw_tags.get('-1')
        tags['sub-plan'] = raw_tags.get('msg-param-sub-plan')

        tags['months'] = raw_tags.get('msg-param-months')
        tags['gift-months'] = raw_tags.get('msg-param-gift-months')
        tags['multimonth-duration'] = '-1'
        tags['multimonth-tenure'] = '-1'
        tags['streak-months'] = '-1'
        tags['share-streak'] = '-1'
        tags['cumulative'] = '-1'
        tags['msg-id'] = raw_tags.get('source-msg-id', raw_tags.get('msg-id'))

        return tags
    
    def _parseSubmysterygift(self, raw_tags:Dict[str, str], room:str) -> Dict[str,str]:
        """Parse submysterygift specific tags"""

        tags = {}

        if 'source-room-id' in raw_tags:
            tags['room-id'] = raw_tags.get('source-room-id')
            tags['room-name'] = '#unknown'
        else:
            tags['room-id'] = raw_tags.get('room-id')
            tags['room-name'] = room

        tags['user-id'] = raw_tags.get('user-id')
        tags['display-name'] = raw_tags.get('display-name')
        tags['username'] = raw_tags.get('display-name').lower()
        
        tags['color'] = raw_tags.get('color')
        tags['badges'] = raw_tags.get('source-badges', raw_tags.get('badges'))
        tags['badge-info'] = raw_tags.get('source-badge-info', raw_tags.get('badge-info'))        
        tags['turbo'] = '-1'
        
        tags['sub'] = raw_tags.get('subscriber', '0')
        tags['vip'] = raw_tags.get('vip', '0')
        tags['mod'] = raw_tags.get('mod', '0')
        tags['user-type'] = raw_tags.get('user-type')

        tags['gift-id'] = raw_tags.get('msg-param-community-gift-id', 'null')
        tags['gift-count'] = raw_tags.get('msg-param-mass-gift-count')
        tags['gifter-total'] = raw_tags.get('msg-param-sender-count')
        tags['sub-plan'] = raw_tags.get('msg-param-sub-plan')

        tags['months'] = '-1'
        tags['gift-months'] = '1'
        tags['multimonth-duration'] = '-1'
        tags['multimonth-tenure'] = '-1'
        tags['streak-months'] = '-1'
        tags['share-streak'] = '-1'
        tags['cumulative'] = '-1'
        tags['msg-id'] = raw_tags.get('source-msg-id', raw_tags.get('msg-id'))

        return tags