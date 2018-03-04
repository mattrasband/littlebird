import asyncio
import json
from abc import ABC, abstractmethod
from asyncio import BaseEventLoop
from typing import Any, AsyncIterable, Dict, List, Optional, Union
from urllib.parse import urlencode

from aiohttp import ClientSession
from oauthlib.oauth1 import Client as OAuth1Client

from .urls import UrlEnum


class AbstractAsyncHttpClient(ABC):
    __slots__ = ('_loop', '_client')

    def __init__(self, *, loop: Optional[BaseEventLoop] = None):
        self._loop = loop or asyncio.get_event_loop()
        self._client = ClientSession(loop=self._loop)

    def __del__(self):
        self._loop.run_until_complete(self._client.close())

    @abstractmethod
    async def stream(self, url: UrlEnum, body=None,
                     method='post') -> AsyncIterable:
        """"""

    @abstractmethod
    async def get(self, url: UrlEnum,
                  params) -> Union[List[Any], Dict[str, Any]]:
        """"""


class OAuth1HttpClient(AbstractAsyncHttpClient):
    """Client for handling oauth1 related actions. This is
    required for any endpoints that require the user-context
    that is unattended or application-only endpoints."""
    __slots__ = ('_oauth_client',)

    def __init__(self, consumer_key: str, consumer_secret: str, *,
                 access_token: Optional[str] = None,
                 access_token_secret: Optional[str] = None):
        super().__init__()
        self._oauth_client = OAuth1Client(
            consumer_key,
            client_secret=consumer_secret,
            resource_owner_key=access_token,
            resource_owner_secret=access_token_secret
        )

    async def stream(self, url, body=None, method='post'):
        url, headers, body = self._oauth_client.sign(
            url.absolute,
            headers={} if body is None else {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body=body,
            http_method=method.upper(),
        )
        async with self._client.request(method.upper(), url,
                                        headers=headers,
                                        data=body) as r:
            r.raise_for_status()
            async for line in r.content:
                if not line.strip():
                    continue
                yield json.loads(line)

    async def get(self, url, body):
        body = {k: v for k, v in body.items() if v is not None}
        url, headers, _ = self._oauth_client.sign(
            url.absolute + (f'?{urlencode(body)}' if body else ''),
            http_method='GET',
        )
        async with self._client.get(url, headers=headers) as r:
            r.raise_for_status()
            return await r.json()


# TODO
# class OAuth2Client(AbstractAsyncHttpClient):
#     pass
