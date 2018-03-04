from enum import Enum
from typing import AsyncIterable, List, Optional

from . import urls, web


class FilterLevel(Enum):
    NONE = 'none'
    LOW = 'low'
    MEDIUM = 'medium'


class LittleBird:
    __slots__ = ('_client',)

    def __init__(self, client: web.AbstractAsyncHttpClient):
        self._client = client

    async def filter(self, *,
                     track: Optional[List[str]] = None,
                     follow: Optional[List[str]] = None,
                     locations: Optional[List[str]] = None,
                     filter_level: FilterLevel = FilterLevel.NONE,
                     stall_warnings: bool = True) -> AsyncIterable:
        """Follow the statuses filtering api

        https://developer.twitter.com/en/docs/tweets/filter-realtime/api-reference/post-statuses-filter.html

        :param follow: List of user ids to follow.
        :param track: List of keywords (or phrases) to track.
        :param locations: List of bounding boxes to track
        :param stall_warnings: Whether or not to warn the caller about stalls
                               when falling behind the twitter real time queue
        :param filter_level: Filter status update frequency
        """
        body = {
            'filter_level': filter_level.value,
            'stall_warnings': 'true' if stall_warnings else 'false',
            'track': ','.join(track) if track is not None else '',
            'follow': ','.join(follow) if follow is not None else '',
            'locations': ','.join(locations) if locations is not None else '',
        }
        async for message in self._client.stream(urls.Streaming.FILTER, body):
            yield message

    async def sample(self) -> AsyncIterable:
        """Retrieve a sampling of public statuses"""
        async for message in self._client.stream(urls.Streaming.SAMPLE):
            yield message

    async def home_timeline(self, *, count: int = 20,
                            since_id: Optional[int] = None,
                            max_id: Optional[int] = None,
                            trim_user: bool = True,
                            exclude_replies: bool = True,
                            include_entities: bool = False):
        """Returns a collection of the most recent Tweets posted
        by the authenticating user and the users they follow."""
        body = {
            'count': count,
            'since_id': since_id,
            'max_id': max_id,
            'trim_user': 'true' if trim_user else 'false',
            'exclude_replies': 'true' if exclude_replies else 'false',
            'include_entities': 'true' if include_entities else 'false',
        }
        return await self._client.get(urls.API.HOME_TIMELINE, body)

    async def user_timeline(self, *,
                            user_id: Optional[str] = None,
                            screen_name: Optional[str] = None,
                            since_id: Optional[int] = None,
                            count: Optional[int] = None,
                            max_id: Optional[int] = None,
                            trim_user: bool = True,
                            exclude_replies: bool = True,
                            include_rts: bool = False):
        body = {
            'user_id': user_id,
            'screen_name': screen_name,
            'since_id': since_id,
            'count': count,
            'max_id': max_id,
            'trim_user': str(trim_user).lower(),
            'exclude_replies': str(exclude_replies).lower(),
            'include_rts': str(include_rts).lower(),
        }
        return await self._client.get(urls.API.USER_TIMELINE, body)

    async def mentions_timeline(self, *,
                                count: Optional[int] = None,
                                since_id: Optional[int] = None,
                                max_id: Optional[int] = None,
                                trim_user: bool = True,
                                include_entities: bool = True):
        body = {
            'count': count,
            'since_id': since_id,
            'max_id': max_id,
            'trim_user': str(trim_user).lower(),
            'include_entities': str(include_entities).lower(),
        }
        return await self._client.get(urls.API.MENTIONS, body)
