littlebird
==========

LittleBird is a Python 3.6+ asynchronous library for accessing twitter utilizing new python features: async generators, type hinting, etc.

Usage
-----

Currently only the oauth1 methods are supported (application only authentication, user account access).

.. code:: python

    import asyncio
    import contextlib

    from littlebird import LittleBird
    from littlebird.web import OAuth1HttpClient

    little_bird = LittleBird(OAuth1HttpClient(
        # required for oauth1 signing:
        consumer_key: str,
        consumer_secret: str,
        # optionally necessary for endpoints requiring a user's scope:
        access_token: Optional[str] = None,
        access_token_secret: Optional[str] = None
    ))

    async def main(little_bird):
        # watch the random sampling of tweets chosen by twitter
        async for tweet in little_bird.sample():
            print(tweet)

    if __name__ == '__main__':
        loop = asyncio.get_event_loop()
        with contextlib.suppress(KeyboardInterrupt):
            loop.run_until_complete(main(little_bird))
