from aiogram import Bot, Dispatcher
from config import BOT_TOKEN, CHANNEL_ID

from handlers import router
from handlers.commands_menu import set_bot_commands
from utils import logger


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.include_router(router)


async def validate_channel():
    if CHANNEL_ID == 0:
        logger.warning("CHANNEL_ID no configurado, el bot funcionara sin cache")
        return

    try:
        chat = await bot.get_chat(CHANNEL_ID)
        logger.info(
            "Canal de cache verificado",
            chat_id=CHANNEL_ID,
            chat_title=chat.title,
        )
    except Exception as e:
        logger.warning(
            "Canal de cache no accesible, la cache se desactivara en este intento",
            error=str(e),
        )


async def main():
    await set_bot_commands(bot)
    await validate_channel()
    await dp.start_polling(bot)