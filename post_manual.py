import asyncio
from telegram_client import TelegramPoster

async def post_manual():
    poster = TelegramPoster()
    
    # Specific tweet details provided by user
    # https://x.com/ChampionsLeague/status/1994073740481831048
    # Since we can't scrape it easily without finding it in feed, 
    # we can allow user to input text/image or hardcode it if they provide details.
    # For now, I'll make it interactive.
    
    print("📝 Manual Telegram Poster")
    text = input("Enter caption/text: ")
    image_url = input("Enter image URL (or leave empty for text only): ")
    
    if not image_url:
        # Handle text only if needed, but poster expects image
        print("This bot is designed for image posts. Please provide an image URL.")
        return

    print("Posting...")
    await poster.post_tweet(text, image_url)

if __name__ == "__main__":
    asyncio.run(post_manual())
