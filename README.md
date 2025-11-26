# Telegram Bot - Champions League Tweet Forwarder

A Python bot that automatically scrapes tweets from the Champions League Twitter account and forwards them to a Telegram channel. The bot filters tweets based on specific criteria and only posts recent, relevant content.

## Features

- 🔍 **Smart Filtering**: Only forwards tweets that meet specific criteria:
  - Must have an image
  - Must have a caption
  - Must not be a video
  - Must not be an ad
  - Must contain the `#UCL` hashtag
  - Must not contain external links
  - Must be less than 12 hours old

- ⏰ **Automated Scheduling**: Runs every 15 minutes (configurable)
- 📝 **Duplicate Prevention**: Tracks seen tweets to avoid reposting
- 🌐 **Browser-based Scraping**: Uses Playwright for reliable Twitter scraping
- ☁️ **Free Deployment**: Can be deployed on GitHub Actions at no cost

## Prerequisites

- Python 3.8+
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))
- Telegram Channel ID
- Twitter/X account username to monitor

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Segniko/Telegram-Bot.git
cd Telegram-Bot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Playwright Browsers

```bash
python -m playwright install
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
TWITTER_USER=ChampionsLeague
BOT_TOKEN=your_telegram_bot_token_here
CHANNEL_ID=@your_channel_id_here
```

**How to get these values:**
- `TWITTER_USER`: The Twitter/X username to monitor (without @)
- `BOT_TOKEN`: Get from [@BotFather](https://t.me/botfather) on Telegram
- `CHANNEL_ID`: Your Telegram channel ID (e.g., `@mychannel` or `-1001234567890`)

## Usage

### Run Locally

```bash
python main.py
```

The bot will:
1. Fetch the latest tweets from the specified account
2. Filter them based on the criteria
3. Post valid tweets to your Telegram channel
4. Exit (when using GitHub Actions) or sleep for 15 minutes (if running continuously)

### Run Continuously (Local)

If you want to run the bot continuously on your local machine, you can modify `main.py` to add back the `while True` loop and `asyncio.sleep()`.

## Deployment

### Option 1: GitHub Actions (Recommended - Free)

GitHub Actions allows you to run the bot for free on a schedule.

1. **Push your code to GitHub** (without the `.env` file)

2. **Add GitHub Secrets**:
   - Go to your repository → Settings → Secrets and variables → Actions
   - Add the following secrets:
     - `TWITTER_USER`
     - `BOT_TOKEN`
     - `CHANNEL_ID`

3. **Create the workflow file** (`.github/workflows/bot.yml`):

```yaml
name: Telegram Bot

on:
  schedule:
    - cron: '*/15 * * * *'  # Runs every 15 minutes
  workflow_dispatch:  # Allows manual trigger

jobs:
  run-bot:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        playwright install --with-deps chromium
    
    - name: Run bot
      env:
        TWITTER_USER: ${{ secrets.TWITTER_USER }}
        BOT_TOKEN: ${{ secrets.BOT_TOKEN }}
        CHANNEL_ID: ${{ secrets.CHANNEL_ID }}
      run: python main.py
    
    - name: Commit seen tweets
      run: |
        git config --local user.email "action@github.com"
        git config --local user.name "GitHub Action"
        git add seen_tweets.json
        git diff --quiet && git diff --staged --quiet || git commit -m "Update seen tweets"
        git push
```

4. **Enable Actions**: Go to the Actions tab in your repository and enable workflows.

### Option 2: Oracle Cloud (Free VPS)

Oracle Cloud offers a generous free tier with powerful VMs.

1. Sign up for [Oracle Cloud Free Tier](https://www.oracle.com/cloud/free/)
2. Create an Ubuntu VM
3. SSH into the server and run:

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip git -y

# Clone your repository
git clone https://github.com/Segniko/Telegram-Bot.git
cd Telegram-Bot

# Install dependencies
pip3 install -r requirements.txt
playwright install --with-deps chromium

# Create .env file
nano .env
# (Add your environment variables)

# Run the bot
python3 main.py
```

To keep it running 24/7, create a systemd service (see `deployment_guide.md` for details).

## Project Structure

```
Telegram-Bot/
├── main.py              # Main bot logic
├── twitter_client.py    # Twitter scraping functionality
├── telegram_client.py   # Telegram posting functionality
├── filter.py            # Tweet filtering logic
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (not in git)
├── .gitignore          # Git ignore file
├── seen_tweets.json    # Tracks processed tweets
└── README.md           # This file
```

## Configuration

### Adjusting the Check Interval

For GitHub Actions, edit the cron schedule in `.github/workflows/bot.yml`:
- Every 15 minutes: `*/15 * * * *`
- Every 30 minutes: `*/30 * * * *`
- Every hour: `0 * * * *`

### Modifying Filter Criteria

Edit `filter.py` to change what tweets get posted:
- Remove the hashtag requirement
- Change the time limit (currently 12 hours)
- Allow videos or ads
- Modify link detection

## Troubleshooting

### Playwright Browser Not Found
```bash
python -m playwright install
```

### Bot Not Posting
- Check that your Telegram bot has admin rights in the channel
- Verify the `CHANNEL_ID` is correct
- Check the logs for filter reasons

### GitHub Actions Not Running
- Ensure the workflow file is in `.github/workflows/`
- Check that secrets are properly configured
- Verify the repository has Actions enabled

## License

MIT License - feel free to use and modify as needed.

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## Acknowledgments

- Built with [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- Uses [Playwright](https://playwright.dev/) for web scraping
