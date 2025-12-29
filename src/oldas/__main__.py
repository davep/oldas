from asyncio import run
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
    article = await anext(
        Articles.stream(
            session, i="tag:google.com,2005:reader/item/6952dab95f45b77afe000dbf"
        )
    )
    print(article.categories)
    print(await article.mark_read(session))
    article = await anext(
        Articles.stream(
            session, i="tag:google.com,2005:reader/item/6952dab95f45b77afe000dbf"
        )
    )
    print(article.categories)
    print(await article.mark_unread(session))
    article = await anext(
        Articles.stream(
            session, i="tag:google.com,2005:reader/item/6952dab95f45b77afe000dbf"
        )
    )
    print(article.categories)


if __name__ == "__main__":
    run(main())
