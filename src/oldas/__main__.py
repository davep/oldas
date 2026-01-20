from asyncio import run
from os import getenv

from oldas.subscriptions import Subscriptions

from .session import Session


async def main() -> None:
    if token := getenv("TOR_TOKEN"):
        session = Session("test", token)
    else:
        session = await Session("test").login(
            getenv("TOR_USER", ""), getenv("TOR_PASSWORD", "")
        )
    print(
        result := await Subscriptions.add(
            session, "https://lorem-rss.herokuapp.com/feed"
        )
    )
    if result.stream_id:
        print(await Subscriptions.remove(session, result.stream_id))


if __name__ == "__main__":
    run(main())
