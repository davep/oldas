from asyncio import run
from datetime import datetime, timedelta
from os import getenv

from .articles import Articles
from .session import Session


async def main() -> None:
    if token := getenv("TOR_TOKEN"):
        session = Session("test", token)
    else:
        session = await Session("test").login(
            getenv("TOR_USER", ""), getenv("TOR_PASSWORD", "")
        )
    async for article in Articles.stream_new_since(
        session, datetime.now() - timedelta(days=2)
    ):
        print(f"{article.title} - {article.published} - {article.updated}")


if __name__ == "__main__":
    run(main())
