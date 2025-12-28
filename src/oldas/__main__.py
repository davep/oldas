from asyncio import run
from datetime import datetime, timedelta
from os import getenv

from .articles import Articles
from .session import Session
from .subscriptions import Subscriptions


async def main() -> None:
    if token := getenv("TOR_TOKEN"):
        session = Session("test", token)
    else:
        session = await Session("test").login(
            getenv("TOR_USER", ""), getenv("TOR_PASSWORD", "")
        )
    sample_subscription = (await Subscriptions.load(session))[0]
    articles = await Articles.load_new_since(
        session, datetime.now() - timedelta(hours=5), sample_subscription
    )
    for article in articles:
        print(f"{article.title} - {article.published} - {article.updated}")
    print(f"Subscription ID: {sample_subscription.id}")
    for article in articles:
        print(
            f"Article ID {article.id} relates to subscription {article.origin.stream_id}"
        )
    print(f"Subscription's categories: {sample_subscription.categories}")
    print(f"First article timestamp: {sample_subscription.first_item_time}")


if __name__ == "__main__":
    run(main())
