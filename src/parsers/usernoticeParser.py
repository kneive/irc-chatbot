from .base import BaseParser, ParseResult
from .tags.tagFactory import TagFactory
from typing import Optional, Dict
import traceback


class UsernoticeParser(BaseParser):

    def parseable(self, input:str) -> bool:
        """Check whether the input is parseable by this parser"""

        return ' USERNOTICE ' in input
    
    def parse(self, input:str) -> Optional[ParseResult]:
        """Parse input and return ParseResult or None"""

        tags = {}
        usernotice = 'USERNOTICE'

        try:
            end = input.find(' :tmi.twitch.tv')
            if end == -1:
                raise ValueError("(parse) USERNOTICE message is corrupted: no ' :'")

            raw_tags = self._parseTags(input[1:end])

            # get room-name / #unknown
            idx_start = input.find(' #', end)
            if idx_start == -1:
                raise ValueError("(parse) USERNOTICE message is corrupted: no ' #'")
            
            idx_end = input.find(' ', idx_start+1)

            if (raw_tags.get('msg-id') == 'sharedchatnotice' and
                raw_tags.get('room-id') != raw_tags.get('source-room-id')):
                raw_tags['room-name'] = input[message_start+2:].strip()
                raw_tags['source-room-name'] = '#unknown'
            else:
                if idx_end == -1:
                    raw_tags['room-name'] = input[idx_start+1:].strip()
                    raw_tags['source-room-name'] = '#unknown'
                else:
                    raw_tags['room-name'] = input[idx_start+1:idx_end].strip()
                    raw_tags['source-room-name'] = '#unknown'
                    message_start = input.find(' :', idx_end)
                    raw_tags['message-content'] = input[message_start+2:].strip()

            # replace \\s  
            if raw_tags.get('msg-param-sub-plan-name') is not None:
                raw_tags['msg-param-sub-plan-name'] = raw_tags.get('msg-param-sub-plan-name').replace('\\s', ' ')

            if raw_tags.get('system-msg') is not None:
                raw_tags['system-msg'] = raw_tags.get('system-msg').replace('\\s', ' ')

            if raw_tags.get('msg-param-fun-string') is not None:
                raw_tags['msg-param-fun-string'] = raw_tags.get('msg-param-fun-string').replace('\\s', ' ')

            # DEBUG output
            print(f'{raw_tags['msg-id']}: {raw_tags['room-name']}')

            # what types of USERNOTICE messages to parse
            if raw_tags.get('msg-id') == 'sharedchatnotice':
                if raw_tags.get('source-msg-id') in ['sub', 'resub']:
                    tags = TagFactory.createSubTag(raw_tags)
                    usernotice='SUBSCRIPTION'
                elif raw_tags.get('source-msg-id') == 'subgift':
                    tags = TagFactory.createSubgiftTag(raw_tags)
                    usernotice='SUBGIFT'
                elif raw_tags.get('source-msg-id') == 'submysterygift':
                    tags = TagFactory.createSubmysterygiftTag(raw_tags)
                    usernotice='SUBMYSTERYGIFT'
                elif raw_tags.get('source-msg-id') == 'announcement':
                    tags = TagFactory.createAnnouncementTag(raw_tags)
                    usernotice='ANNOUNCEMENT'
                elif raw_tags.get('source-msg-id') == 'viewermilestone':
                    tags = TagFactory.createViewerMilestoneTag(raw_tags)
                    usernotice='VIEWERMILESTONE'
                elif raw_tags.get('source-msg-id') == 'raid':
                    tags = TagFactory.createRaidTag(raw_tags)
                    usernotice='RAID'
                elif raw_tags.get('source-msg-id') == 'standardpayforward':
                    tags = TagFactory.createStandardPayForwardTag(raw_tags)
                    usernotice='STANDARDPAYFORWARD'
                elif raw_tags.get('source-msg-id') == 'communitypayforward':
                    tags = TagFactory.createCommunityPayForwardTag(raw_tags)
                    usernotice='COMMUNITYPAYFORWARD'
                elif raw_tags.get('source-msg-id') == 'primepaidupgrade':
                    tags = TagFactory.createPrimePaidUpgradeTag(raw_tags)
                    usernotice='PRIMEPAIDUPGRADE'
                elif raw_tags.get('source-msg-id') == 'giftpaidupgrade':
                    tags = TagFactory.createGiftPaidUpgradeTag(raw_tags)
                    usernotice='GIFTPAIDUPGRADE'
                elif raw_tags.get('source-msg-id') == 'onetapgiftredeemed':
                    tags = TagFactory.createOneTapGiftRedeemedTag(raw_tags)
                    usernotice='ONETAPGIFTREDEEMED'
                elif raw_tags.get('source-msg-id') == 'bitsbadgetier': 
                    tags = TagFactory.createBitsBadgeTierTag(raw_tags)
                    usernotice='BITSBADGETIER'

            else:
                if raw_tags.get('msg-id') in ['sub', 'resub']:
                    tags = TagFactory.createSubTag(raw_tags)
                    usernotice='SUBSCRIPTION'
                elif raw_tags.get('msg-id') == 'subgift':
                    tags = TagFactory.createSubgiftTag(raw_tags)
                    usernotice='SUBGIFT'
                elif raw_tags.get('msg-id') == 'submysterygift':
                    tags = TagFactory.createSubmysterygiftTag(raw_tags)
                    usernotice='SUBMYSTERYGIFT'
                elif raw_tags.get('msg-id') == 'announcement':
                    tags = TagFactory.createAnnouncementTag(raw_tags)
                    usernotice='ANNOUNCEMENT'
                elif raw_tags.get('msg-id') == 'viewermilestone':
                    tags = TagFactory.createViewerMilestoneTag(raw_tags)
                    usernotice='VIEWERMILESTONE'
                elif raw_tags.get('msg-id') == 'raid':
                    tags = TagFactory.createRaidTag(raw_tags)
                    usernotice='RAID'
                elif raw_tags.get('msg-id') == 'standardpayforward':
                    tags = TagFactory.createStandardPayForwardTag(raw_tags)
                    usernotice='STANDARDPAYFORWARD'
                elif raw_tags.get('msg-id') == 'communitypayforward':
                    tags = TagFactory.createCommunityPayForwardTag(raw_tags)
                    usernotice='COMMUNITYPAYFORWARD'
                elif raw_tags.get('msg-id') == 'primepaidupgrade':
                    tags = TagFactory.createPrimePaidUpgradeTag(raw_tags)
                    usernotice='PRIMEPAIDUPGRADE'
                elif raw_tags.get('msg-id') == 'giftpaidupgrade':
                    tags = TagFactory.createGiftPaidUpgradeTag(raw_tags)
                    usernotice='GIFTPAIDUPGRADE'
                elif raw_tags.get('msg-id') == 'onetapgiftredeemed':
                    tags = TagFactory.createOneTapGiftRedeemedTag(raw_tags)
                    usernotice='ONETAPGIFTREDEEMED'
                elif raw_tags.get('msg-id') == 'bitsbadgetier': 
                    tags = TagFactory.createBitsBadgeTierTag(raw_tags)
                    usernotice='BITSBADGETIER'
            
            # not parseable
            if tags == {} or usernotice == 'USERNOTICE':
                raise ValueError(f'(parse) USERNOTICE message not parsed:\n {tags}\n {usernotice}')

            return ParseResult(usernotice,
                               tags,
                               input)


        except Exception as e:
            print(input)
            print(f'(parse) USERNOTICE is corrupted: {e}, ({tags})')
            print(f'Traceback: {traceback.format_exc()}')
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
            raise ValueError(f'(_parseTags) PRIVMSG message is corrupted: ({tags.items()})')