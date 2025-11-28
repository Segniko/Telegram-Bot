import asyncio
import os
import sys
import json
from datetime import datetime
from twitter_client import TwitterScraper
from telegram_client import TelegramPoster
from filter import is_valid_tweet

SEEN_TWEETS_FILE = 'seen_tweets.json'
CHECK_INTERVAL_MINUTES = 15

def load_seen_tweets():
    if os.path.exists(SEEN_TWEETS_FILE):
        with open(SEEN_TWEETS_FILE, 'r') as f:
            return set(json.load(f))
    return set()

def save_seen_tweets(seen_ids):
    with open(SEEN_TWEETS_FILE, 'w') as f:
        json.dump(list(seen_ids), f)

async def check_and_post():
    """Check for new tweets and post them if valid"""
    scraper = TwitterScraper()
    poster = TelegramPoster()
    seen_tweets = load_seen_tweets()
    
    max_retries = 3
    retry_delay = 5  # seconds

    for attempt in range(max_retries):
        try:
            print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Fetching tweets... (Attempt {attempt + 1}/{max_retries})")
            tweets = await scraper.fetch_latest_tweets()
            print(f"Fetched IDs: {[t['id'] for t in tweets]}")
            
            new_posts_found = 0
            
            # Process tweets from oldest to newest to maintain order if multiple are new
            # But the scraper returns newest first, so we reverse
            for tweet in reversed(tweets):
                tweet_id = tweet['id']
                
                if tweet_id in seen_tweets:
                    continue

                print(f"Checking tweet {tweet_id}...")
                is_valid, reason = is_valid_tweet(tweet)
                
                if is_valid:
                    print(f"✅ Valid tweet found: {tweet['text'][:50]}...")
                    success = await poster.post_tweet(tweet['text'], tweet['image_url'])
                    
                    if success:
                        seen_tweets.add(tweet_id)
                        save_seen_tweets(seen_tweets)
                        new_posts_found += 1
                        print(f"📤 Posted to Telegram!")
                    else:
                        print(f"⚠️ Failed to post tweet {tweet_id}")
                else:
                    print(f"⏭️  Skipping tweet {tweet_id}: {reason}")
                    # We still mark it as seen so we don't re-process it
                    seen_tweets.add(tweet_id)
                    save_seen_tweets(seen_tweets)

            if new_posts_found == 0:
                print(f"No new posts found in the last 1 hour.")
            else:
                print(f"Posted {new_posts_found} new tweet(s).")
            
            # Success - break out of retry loop
            break

        except Exception as e:
            print(f"❌ Error in check loop (Attempt {attempt + 1}/{max_retries}): {e}")
            
            if attempt < max_retries - 1:
                wait_time = retry_delay * (2 ** attempt)  # Exponential backoff
                print(f"⏳ Retrying in {wait_time} seconds...")
                await asyncio.sleep(wait_time)
            else:
                print(f"❌ Failed after {max_retries} attempts. Will try again in next cycle.")
                import traceback
                traceback.print_exc()

async def main():
    # Check for run-once flag (for GitHub Actions)
    run_once = '--once' in sys.argv

    print("="*60)
    print("🤖 Telegram Bot Started")
    if run_once:
        print("🚀 Mode: Run Once (GitHub Actions)")
    else:
        print("🔄 Mode: Continuous Loop")
        print(f"⏰ Checking every {CHECK_INTERVAL_MINUTES} minutes")
    
    print(f"🕐 Time window: Last 1 hour")
    print("="*60)
    
    while True:
        await check_and_post()
        
        if run_once:
            print("✅ Run once completed. Exiting.")
            break
            
        print(f"\n💤 Sleeping for {CHECK_INTERVAL_MINUTES} minutes...")
        print(f"Next check at: {(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')}")
        print("-"*60)
        
        await asyncio.sleep(CHECK_INTERVAL_MINUTES * 60)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n🛑 Bot stopped by user.")
