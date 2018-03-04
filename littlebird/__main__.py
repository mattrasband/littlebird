import asyncio
import json
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from contextlib import suppress

try:
    import uvloop
except ImportError:
    pass
else:
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
from pygments import formatters, highlight, lexers

from .client import LittleBird
from .web import OAuth1HttpClient


async def _main(little_bird: LittleBird) -> None:
    async for status in little_bird.filter(track=[
        '#BuzzWord'
    ]):
        str_status = json.dumps(status, sort_keys=True, indent=4)
        print(highlight(str_status, lexers.JsonLexer(),
                        formatters.TerminalFormatter()))

    # async for status in little_bird.sample():
    #     pprint(status)
    # pprint(await little_bird.home_timeline())
    # pprint(await little_bird.user_timeline(screen_name='dhh'))
    # pprint(await little_bird.mentions_timeline())


def main():
    parser = ArgumentParser(prog='littlebird',
                            description='Stream tweets from twitter in real-time',  # noqa
                            formatter_class=ArgumentDefaultsHelpFormatter)

    subparsers = parser.add_subparsers(title='Authentication methods')

    oauth1_parser = subparsers.add_parser(
        'oauth1',
        help='Use OAuth1 for application-only or unattended user access',
        description='Use credentials from https://apps.twitter.com. If '
                    'unattended user access is necessary, generate a user '
                    ' access token.',
    )
    oauth1_parser.add_argument('--consumer-key', '-k', type=str, required=True,
                               help='OAuth 1.0 Consumer Key')
    oauth1_parser.add_argument('--consumer-secret', '-s', type=str,
                               required=True, help='OAuth 1.0 Consumer Secret')
    oauth1_parser.add_argument('--access-token', type=str,
                               help='User access token')
    oauth1_parser.add_argument('--access-token-secret', type=str,
                               help='User access token secret')
    # the parser is a factory for an HTTP client for LittleBird to use
    oauth1_parser.set_defaults(func=lambda args: OAuth1HttpClient(
        consumer_key=args.consumer_key,
        consumer_secret=args.consumer_secret,
        access_token=args.access_token,
        access_token_secret=args.access_token_secret)
    )
    args = parser.parse_args()

    loop = asyncio.get_event_loop()
    http_client = args.func(args)
    little_bird = LittleBird(http_client)

    with suppress(KeyboardInterrupt):
        loop.run_until_complete(_main(little_bird))


if __name__ == '__main__':
    main()
