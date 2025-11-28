import asyncio
from telegram_client import TelegramPoster

async def post_manual():
    poster = TelegramPoster()
    
    # Specific tweet details provided by user
    
    print("📝 Manual Telegram Poster")
    print("Enter caption/text (Type a single dot '.' on a line to finish):")
    lines = []
    while True:
        line = input()
        if line == ".":
            break
        lines.append(line)
    text = "\n".join(lines)
    image_url = input("Enter image URL (or leave empty for text only): ")
    
    if not image_url:
        # Handle text only if needed, but poster expects image
        print("This bot is designed for image posts. Please provide an image URL.")
        return

    print("Posting...")
    await poster.post_tweet(text, image_url)

if __name__ == "__main__":
    asyncio.run(post_manual())
