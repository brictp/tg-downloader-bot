import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(override=True)

SHAZAM_API_TOKEN = os.getenv("SHAZAM_API_TOKEN")
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = os.getenv("OWNER_ID")
RATE_LIMIT_SECONDS = int(os.getenv("RATE_LIMIT_SECONDS", "30"))
MAX_FILE_SIZE_VIDEO = int(os.getenv("MAX_FILE_SIZE_VIDEO", "45")) * 1024 * 1024
MAX_FILE_SIZE_AUDIO = int(os.getenv("MAX_FILE_SIZE_AUDIO", "6")) * 1024 * 1024

CHANNEL_ID = int(os.getenv("CHANNEL_ID", "0"))
VIDEO_CACHE_FILE = Path(os.getenv("VIDEO_CACHE_FILE", "data/video_cache.json"))

DEV_MODE = os.getenv("DEV_MODE", "false").lower() in ("1", "true", "yes", "on")
LOG_FILE = Path(os.getenv("LOG_FILE", "logs/bot.log"))