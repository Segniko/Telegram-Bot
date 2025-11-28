import asyncio
from playwright.async_api import async_playwright
import os

AUTH_FILE = 'auth.json'

async def login():
    print("="*60)
    print("🔐 Twitter Login Helper")
    print("="*60)
    print("This script will open a browser window.")
    print("1. Please log in to your Twitter/X account manually.")
    print("2. Handle any 2FA or email verification codes.")
    print("3. Once you are on your home feed, come back here and press ENTER.")
    print("="*60)

    async with async_playwright() as p:
        # Launch headed browser so user can interact
        # Add args to bypass "browser not supported"
        browser = await p.chromium.launch(
            headless=False,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
                '--disable-infobars',
            ]
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={'width': 1280, 'height': 720}
        )
        page = await context.new_page()

        # Remove webdriver property to avoid detection
        await page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)

        try:
            print("\n🚀 Opening Twitter home page...")
            print("👉 Please click 'Log in' (or 'Sign in') and log in to your account.")
            await page.goto("https://x.com")
            
            # Wait for user to complete login
            input("\n✅ Press ENTER here after you have successfully logged in...")
            
            # Save storage state
            print(f"\n💾 Saving session to {AUTH_FILE}...")
            await context.storage_state(path=AUTH_FILE)
            print("✅ Session saved successfully!")
            print("You can now run the bot.")

        except Exception as e:
            print(f"\n❌ Error: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(login())
