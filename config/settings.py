import os
from dotenv import load_dotenv

load_dotenv(override=True)

SHAZAM_API_TOKEN = os.getenv("SHAZAM_API_TOKEN")
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = os.getenv("OWNER_ID")
RATE_LIMIT_SECONDS = int(os.getenv("RATE_LIMIT_SECONDS", "30"))
MAX_FILE_SIZE_VIDEO = int(os.getenv("MAX_FILE_SIZE_VIDEO", "45")) * 1024 * 1024
MAX_FILE_SIZE_AUDIO = int(os.getenv("MAX_FILE_SIZE_AUDIO", "6")) * 1024 * 1024