import asyncio
from twitter_client import TwitterScraper

async def test():
    scraper = TwitterScraper()
    print("Testing scraper...")
    tweets = await scraper.fetch_latest_tweets()
    print(f"Fetched {len(tweets)} tweets.")
    for t in tweets:
        print(f"ID: {t['id']}, Text: {t['text'][:50]}..., Image: {t['has_image']}")

if __name__ == "__main__":
    asyncio.run(test())
