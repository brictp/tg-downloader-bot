from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeChat
from aiogram.exceptions import TelegramBadRequest

from config.settings import OWNER_ID

from utils import logger


async def set_bot_commands(bot):
    public = [
        BotCommand(command="start", description="Iniciar el bot"),
        BotCommand(command="owner", description="Info del creador"),
        BotCommand(command="getid", description="Obtener tu ID de Telegram"),
        BotCommand(command="d", description="[Grupos] Descargar video desde URL"),
        BotCommand(command="getsong", description="🔴 No disponible"),
        BotCommand(command="adminhelp", description="Comandos de administración"),
        BotCommand(command="getuseradmins", description="[Admin] Listar admins"),
        BotCommand(command="getbotusers", description="[Admin] Listar usuarios"),
    ]
    await bot.set_my_commands(public, scope=BotCommandScopeDefault())

    owner = [
        BotCommand(command="start", description="Iniciar el bot"),
        BotCommand(command="owner", description="Info del creador"),
        BotCommand(command="getid", description="Obtener tu ID de Telegram"),
        BotCommand(command="d", description="[Grupos] Descargar video desde URL"),
        BotCommand(command="getsong", description="🔴 No disponible"),
        BotCommand(command="adminhelp", description="Comandos de administración"),
        BotCommand(command="idgrupo", description="Obtener ID del grupo"),
        BotCommand(command="allowuser", description="[Admin] Permitir usuario"),
        BotCommand(command="removeuser", description="[Admin] Remover usuario"),
        BotCommand(command="allowadmin", description="[Owner] Promover admin"),
        BotCommand(command="removeadmin", description="[Owner] Remover admin"),
        BotCommand(command="clearcache", description="[Owner] Limpiar caché de videos"),
        BotCommand(command="getuseradmins", description="[Admin] Listar admins"),
        BotCommand(command="getbotusers", description="[Admin] Listar usuarios"),
    ]
    try:
        await bot.set_my_commands(owner, scope=BotCommandScopeChat(chat_id=int(OWNER_ID)))
    except TelegramBadRequest as e:
        logger.warning(
            "No se pudo setear comandos del owner: chat no disponible aun",
            error=str(e),
        )