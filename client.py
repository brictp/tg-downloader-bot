from aiogram import Bot, Dispatcher
from config import BOT_TOKEN

from handlers import router
from handlers.commands_menu import set_bot_commands


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.include_router(router)


async def main():
    await set_bot_commands(bot)
    await dp.start_polling(bot)