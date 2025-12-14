import os
from dotenv import load_dotenv

load_dotenv(override=True)

SHAZAM_API_TOKEN = os.getenv("SHAZAM_API_TOKEN")
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = os.getenv("OWNER_ID")
