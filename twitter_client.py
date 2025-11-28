import asyncio
from playwright.async_api import async_playwright
import os
from dotenv import load_dotenv

load_dotenv()

class TwitterScraper:
    def __init__(self):
        self.username = os.getenv('TWITTER_USER')
    async def fetch_latest_tweets(self):
        """
        Scrapes the latest tweets from the user's profile.
        Uses authenticated session if available to get accurate chronological results via Search.
        """
        tweets_data = []
        
        # Use Search URL with f=live to get reverse chronological order
        # This works reliably ONLY when authenticated
        self.url = f"https://x.com/search?q=from%3A{self.username}&src=typed_query&f=live"
        
        async with async_playwright() as p:
            # Check for auth file
            auth_file = 'auth.json'
            if os.path.exists(auth_file):
                print(f"🔑 Loading authenticated session from {auth_file}...")
                context_options = {'storage_state': auth_file}
            else:
                print("⚠️ No auth file found! Scraping will likely fail or show old tweets.")
                print("   Run 'python login.py' to authenticate.")
                context_options = {}

            # Launch browser
            browser = await p.chromium.launch(
                headless=True,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-dev-shm-usage',
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-web-security',
                ]
            )
            
            # Create context with auth if available
            context = await browser.new_context(
                **context_options,
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                viewport={'width': 1920, 'height': 1080},
                locale='en-US',
                timezone_id='America/New_York',
            )
            
            # Add extra headers
            await context.set_extra_http_headers({
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            })
            
            page = await context.new_page()
            
            # Remove webdriver property
            await page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            """)

            try:
                print(f"Navigating to {self.url}...")
                await page.goto(self.url, wait_until='domcontentloaded', timeout=90000)
                
                # Wait a bit for dynamic content
                await asyncio.sleep(3)
                
                # Wait for tweets to load with a longer timeout
                await page.wait_for_selector('article[data-testid="tweet"]', timeout=45000)
                
                # Scroll down to load more tweets
                for _ in range(10):
                    await page.mouse.wheel(0, 1000)
                    await asyncio.sleep(2)

                # Get all tweet elements
                tweets = await page.locator('article[data-testid="tweet"]').all()
                
                print(f"Found {len(tweets)} tweets. Parsing...")

                for tweet in tweets[:50]: # Check top 50 tweets
                    try:
                        # Extract Text
                        text_element = tweet.locator('div[data-testid="tweetText"]')
                        text = await text_element.inner_text() if await text_element.count() > 0 else ""
                        
                        # Extract ID (from the time element link)
                        time_element = tweet.locator('time')
                        timestamp = await time_element.get_attribute('datetime') if await time_element.count() > 0 else ""
                        # Construct a pseudo-ID from timestamp or find the status link
                        # Ideally we find the link: /username/status/123456...
                        link_element = tweet.locator('a[href*="/status/"]').first
                        href = await link_element.get_attribute('href') if await link_element.count() > 0 else ""
                        tweet_id = href.split('/')[-1] if href else timestamp

                        # Check for Images
                        photo_elements = tweet.locator('div[data-testid="tweetPhoto"] img')
                        photos = []
                        count = await photo_elements.count()
                        for i in range(count):
                            src = await photo_elements.nth(i).get_attribute('src')
                            if src:
                                photos.append(src)
                        
                        has_image = len(photos) > 0
                        image_url = photos[0] if has_image else None

                        # Check for Video
                        video_element = tweet.locator('div[data-testid="videoPlayer"]')
                        is_video = await video_element.count() > 0

                        # Check for Ad (Promoted)
                        # Ads usually have a "Promoted" text at the bottom, but on profile pages it's rare.
                        # We can check for the "Ad" label if it exists.
                        
                        tweets_data.append({
                            'id': tweet_id,
                            'text': text,
                            'has_image': has_image,
                            'image_url': image_url,
                            'is_video': is_video,
                            'is_video': is_video,
                            'is_ad': False, # Placeholder, hard to detect reliably without specific selector
                            'timestamp': timestamp
                        })
                    except Exception as e:
                        print(f"Error parsing tweet: {e}")
                        continue

            except Exception as e:
                print(f"Error scraping Twitter: {e}")
            finally:
                await browser.close()
        
        return tweets_data

# Test
if __name__ == "__main__":
    scraper = TwitterScraper()
    # tweets = asyncio.run(scraper.fetch_latest_tweets())
    # print(tweets)
