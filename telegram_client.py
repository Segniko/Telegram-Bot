import os
import asyncio
from telegram import Bot
from dotenv import load_dotenv

load_dotenv()

class TelegramPoster:
    def __init__(self):
        self.token = os.getenv('BOT_TOKEN')
        self.channel_id = os.getenv('CHANNEL_ID')
        self.bot = Bot(token=self.token)

    async def post_tweet(self, text, image_url):
        """
        Posts a tweet (image + caption) to the Telegram channel.
        """
        try:
            print(f"Posting to {self.channel_id}...")
            await self.bot.send_photo(
                chat_id=self.channel_id,
                photo=image_url,
                caption=text
            )
            print("Successfully posted.")
        except Exception as e:
            print(f"Error posting to Telegram: {e}")

# Test
if __name__ == "__main__":
    poster = TelegramPoster()
    # asyncio.run(poster.post_tweet("Test Caption", "https://via.placeholder.com/150"))
