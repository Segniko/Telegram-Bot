import asyncio
import os
import json
from twitter_client import TwitterScraper
from telegram_client import TelegramPoster
from filter import is_valid_tweet

SEEN_TWEETS_FILE = 'seen_tweets.json'

def load_seen_tweets():
    if os.path.exists(SEEN_TWEETS_FILE):
        with open(SEEN_TWEETS_FILE, 'r') as f:
            return set(json.load(f))
    return set()

def save_seen_tweets(seen_ids):
    with open(SEEN_TWEETS_FILE, 'w') as f:
        json.dump(list(seen_ids), f)

async def main():
    print("Starting Telegram Bot...")
    scraper = TwitterScraper()
    poster = TelegramPoster()
    seen_tweets = load_seen_tweets()

    try:
        print("Fetching tweets...")
        tweets = await scraper.fetch_latest_tweets()
        
        # Process tweets from oldest to newest to maintain order if multiple are new
        # But the scraper returns newest first, so we reverse
        for tweet in reversed(tweets):
            tweet_id = tweet['id']
            
            if tweet_id in seen_tweets:
                continue

            print(f"Checking tweet {tweet_id}...")
            is_valid, reason = is_valid_tweet(tweet)
            
            if is_valid:
                print(f"Valid tweet found: {tweet['text'][:30]}...")
                await poster.post_tweet(tweet['text'], tweet['image_url'])
                seen_tweets.add(tweet_id)
                save_seen_tweets(seen_tweets)
            else:
                print(f"Skipping tweet {tweet_id}: {reason}")
                # We still mark it as seen so we don't re-process it
                seen_tweets.add(tweet_id)
                save_seen_tweets(seen_tweets)

        print("Finished processing tweets.")

    except Exception as e:
        print(f"Error in main loop: {e}")

if __name__ == "__main__":
    asyncio.run(main())
