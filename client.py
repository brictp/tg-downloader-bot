from aiogram import Bot, Dispatcher
from os import getenv
from dotenv import load_dotenv

from handlers import router

load_dotenv()
BOT_TOKEN = getenv("BOT_TOKEN")

# Crear el bot y el dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.include_router(router)


# Función principal para iniciar el bot
async def main():
    await dp.start_polling(bot)
