# Telegram Downloader Bot

A Python Telegram bot that downloads videos and audio from URLs, with song identification capabilities using the Shazam API.

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram-Bot-26A5E4?logo=telegram&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)

## Features

- 📥 **Download videos** from various platforms (YouTube, etc.)
- 🎵 **Download audio** and convert to MP3/WAV
- 🎶 **Song identification** using Shazam API
- 🤖 **Telegram integration** with inline commands
- 🗃️ **Video cache via archive channel**: videos are uploaded to a private channel and re-sent from there, so repeat requests are instant and the archive is kept for recovery
- 📁 **Automatic file cleanup** after sending
- 🐳 **Docker support** for easy deployment

## Commands

- `/start` - Start the bot
- `/idgrupo` - Get group/chat ID
- Send any URL - Bot will automatically detect and download the media
- For song identification, the bot will process audio and return song name + artist

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/tg-downloader-bot.git
   cd tg-downloader-bot
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env
   ```
   
   Configure your `.env` file:
   ```env
   BOT_TOKEN=your_telegram_bot_token
   SHAZAM_API_TOKEN=your_shazam_api_token
   CHANNEL_ID=your_archive_channel_id
   ```

4. **Run the bot:**
   ```bash
   python main.py
   ```

## Docker Deployment

```bash
# Build image
docker build -t tg-downloader-bot .

# Run container
docker run -d --env-file .env tg-downloader-bot
```

## API Keys Setup

1. **Telegram Bot Token:**
   - Contact [@BotFather](https://t.me/botfather) on Telegram
   - Create a new bot and get your token

2. **Shazam API Token:**
   - Sign up at [RapidAPI](https://rapidapi.com/)
   - Subscribe to the Shazam API
   - Get your API key

## Tech Stack

- **aiogram** - Telegram Bot API framework
- **yt-dlp** - Media downloader
- **pydub** - Audio processing
- **requests** - HTTP requests for Shazam API
- **python-dotenv** - Environment variables management

## Project Structure

```
├── main.py              # Entry point
├── client.py            # Bot initialization
├── config/
│   └── settings.py      # Environment configuration
├── handlers/
│   ├── commands.py      # Bot command handlers
│   ├── router.py        # Message routing
│   └── mixins/          # Info, download & admin logic
└── utils/
    ├── downloader.py    # Media download logic
    ├── cache.py         # Video cache index (channel-based)
    ├── url_utils.py     # URL canonicalization for cache keys
    ├── get_song_name.py # Shazam integration
    ├── enums.py         # Media format enums
    └── logger.py        # Error logging
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## License

This project is licensed under the MIT License.
