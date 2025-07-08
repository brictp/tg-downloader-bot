import os
from dotenv import load_dotenv

load_dotenv()

SHAZAM_API_TOKEN = os.getenv("SHAZAM_API_TOKEN")
BOT_TOKEN = os.getenv("BOT_TOKEN")
