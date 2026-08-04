from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from aiogram import Router

from handlers import BotHandlers
from handlers.middleware import AuthContextMiddleware
from handlers.throttling import ThrottlingMiddleware
from utils import get_params_from_message

router = Router()
router.message.outer_middleware(AuthContextMiddleware())
router.message.outer_middleware(ThrottlingMiddleware())

bot_handler = BotHandlers()


@router.message(Command(commands=["start"]))
async def start_bot(message: Message):
    await bot_handler.start_bot(message)


@router.message(Command(commands=["owner"]))
async def owner_info(message: Message):
    await bot_handler.get_owner(message)


@router.message(Command(commands=["getid"]))
async def user_id(message: Message):
    await bot_handler.get_user_id(message)


@router.message(Command(commands=["idgrupo"]))
async def group_id(message: Message):
    await bot_handler.get_group_id(message)


@router.message(Command(commands=["getsong"]))
async def get_song(message: Message):
    await message.reply("Comando /getsong no disponible por el momento")


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


@router.message(Command(commands=["clearcache"]))
async def clear_cache(message: Message):
    await bot_handler.clear_cache(message)


@router.message(Command(commands=["getuseradmins"]))
async def get_admins(message: Message):
    await bot_handler.list_admins(message)


@router.message(Command(commands=["getbotusers"]))
async def get_users(message: Message):
    await bot_handler.list_users(message)


@router.message(Command(commands=["d"]))
async def detect_and_download(message: Message):
    await bot_handler.search_and_download(message)


@router.message(Command(commands=["adminhelp"]))
async def admin_help(message: Message):
    await bot_handler.admin_help(message)


@router.message()
async def auto_detect_url(message: Message):
    if message.chat.type != "private":
        return
    url, _ = get_params_from_message(message.text or "")
    if url:
        await bot_handler.search_and_download(message)