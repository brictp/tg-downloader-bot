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


@router.message(Command(commands=["getsong"]))
async def get_song(message: Message):
    await bot_handler.get_song_name(message)


@router.message(Command(commands=["allowuser"]))
async def allow_user_download_videos(message: Message):
    await bot_handler.add_user(message)


@router.message(Command(commands=["removeuser"]))
async def remove_user(message: Message):
    await bot_handler.remove_user(message)


@router.message(Command(commands=["allowadmin"]))
async def allow_user_add_admins(message: Message):
    await bot_handler.add_admin(message)


@router.message(Command(commands=["removeadmin"]))
async def remove_admins(message: Message):
    await bot_handler.remove_user(message)


@router.message(Command(commands=["d"]))
async def detect_and_download(message: Message):
    await bot_handler.search_and_download(message)
