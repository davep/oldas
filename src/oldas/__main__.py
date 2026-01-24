from asyncio import run
from os import getenv

from oldas import Subscriptions

from .session import Session


async def main() -> None:
    if token := getenv("TOR_TOKEN"):
        session = Session("test", token)
    else:
        session = await Session("test").login(
            getenv("TOR_USER", ""), getenv("TOR_PASSWORD", "")
        )
    for subscription in await Subscriptions.load(session):
        print(f"{subscription.title} {subscription.folder_id}")


if __name__ == "__main__":
    run(main())
