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

            idx_start = input.find(' #', end)
            if idx_start == -1:
                raise ValueError("(parse) USERNOTICE message is corrupted: no ' #'")
            
            idx_end = input.find(' ', idx_start+1)

            if raw_tags.get('msg-id') == 'sharedchatnotice':
                raw_tags['room-name'] = '#unkown'
            else:
                if idx_end == -1:
                    raw_tags['room-name'] = input[idx_start+1:].strip()
                else:
                    raw_tags['room-name'] = input[idx_start+1:idx_end].strip()
                    message_start = input.find(' :', idx_end)
                    raw_tags['message-content'] = input[message_start+2:].strip()

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