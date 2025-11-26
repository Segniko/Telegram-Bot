import asyncio
from twitter_client import TwitterScraper
import json

async def main():
    scraper = TwitterScraper()
    print("Fetching tweets...")
    tweets = await scraper.fetch_latest_tweets()
    
    print("\nFetched Tweets:")
    for tweet in tweets:
        print(f"ID: {tweet['id']}, Text: {tweet['text'][:30]}...")

    with open('seen_tweets.json', 'r') as f:
        seen = json.load(f)
    
    print("\nSeen Tweets:")
    print(seen)

    print("\nMatches:")
    for tweet in tweets:
        if tweet['id'] in seen:
            print(f"Tweet {tweet['id']} is in seen_tweets")
        else:
            print(f"Tweet {tweet['id']} is NEW")

if __name__ == "__main__":
    asyncio.run(main())
