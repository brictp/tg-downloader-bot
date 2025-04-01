from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router

from handlers import BotHandlers

router = Router()

bot_handler = BotHandlers()


@router.message(Command(commands=["start"]))
async def start_bot(message: Message):
    await bot_handler.start_bot(message)


@router.message(Command(commands=["idgrupo"]))
async def group_id(message: Message):
    await bot_handler.get_group_id(message)


@router.message()
async def detect_and_download(message: Message):
    await bot_handler.search_and_download(message)
