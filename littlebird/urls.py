from enum import Enum


class UrlEnum(Enum):
    @property
    def absolute(self) -> str:
        raise NotImplementedError


class Streaming(UrlEnum):
    """Urls for streaming"""
    FILTER = '/statuses/filter.json'
    SAMPLE = '/statuses/sample.json'

    @property
    def absolute(self) -> str:
        return f'https://stream.twitter.com/1.1{self.value}'


class API(UrlEnum):
    """Urls for the API"""
    HOME_TIMELINE = '/statuses/home_timeline.json'
    MENTIONS = '/statuses/mentions_timeline.json'
    USER_TIMELINE = '/statuses/user_timeline.json'

    @property
    def absolute(self) -> str:
        return f'https://api.twitter.com/1.1{self.value}'
