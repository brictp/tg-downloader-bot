from aiogram import Bot, Dispatcher
from config import BOT_TOKEN

from handlers import router


# Crear el bot y el dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.include_router(router)


# Función principal para iniciar el bot
async def main():
    await dp.start_polling(bot)
