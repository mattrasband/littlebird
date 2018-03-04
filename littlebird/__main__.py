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

    parser.add_argument('--consumer-key', '-k', type=str, required=True,
                        help='OAuth 1.0 Consumer Key')
    parser.add_argument('--consumer-secret', '-s', type=str,
                        required=True, help='OAuth 1.0 Consumer Secret')
    parser.add_argument('--access-token', type=str, help='User access token')
    parser.add_argument('--access-token-secret', type=str,
                        help='User access token secret')
    args = parser.parse_args()

    loop = asyncio.get_event_loop()
    little_bird = LittleBird(consumer_key=args.consumer_key,
                             consumer_secret=args.consumer_secret,
                             access_token=args.access_token,
                             access_token_secret=args.access_token_secret)

    with suppress(KeyboardInterrupt):
        loop.run_until_complete(_main(little_bird))


if __name__ == '__main__':
    main()
