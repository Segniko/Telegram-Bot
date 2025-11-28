import asyncio
from twitter_client import TwitterScraper

async def test():
    print("Testing Twitter Scraper...")
    scraper = TwitterScraper()
    tweets = await scraper.fetch_latest_tweets()
    
    print(f"\n{'='*80}")
    print(f"Successfully fetched {len(tweets)} tweets!")
    print(f"{'='*80}\n")
    
    for i, tweet in enumerate(tweets[:3], 1):
        print(f"Tweet {i}:")
        print(f"  ID: {tweet['id']}")
        print(f"  Text: {tweet['text'][:100]}...")
        print(f"  Has Image: {tweet['has_image']}")
        print(f"  Timestamp: {tweet['timestamp']}")
        print()

if __name__ == "__main__":
    asyncio.run(test())
