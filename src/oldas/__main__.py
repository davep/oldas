from asyncio import run
from os import getenv

from .folders import Folders
from .session import Session
from .subscriptions import Subscriptions
from .unread import Unread


async def main() -> None:
    if token := getenv("TOR_TOKEN"):
        session = Session("test", token)
    else:
        session = await Session("test").login(
            getenv("TOR_USER", ""), getenv("TOR_PASSWORD", "")
        )
    for subscription in await Subscriptions.load(session):
        print(f"{subscription.title} - {subscription.id}")
    print(await Unread.load(session))
    print(await Folders.load(session))


if __name__ == "__main__":
    run(main())
