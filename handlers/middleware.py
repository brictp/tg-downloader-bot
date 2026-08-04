import re

from aiogram.types import Message
from aiogram import BaseMiddleware
from typing import Callable, Dict, Any, Awaitable

from utils import logger, LogContext
from utils.user_allowed_handler import UserHandler
from config.settings import OWNER_ID

user_handler = UserHandler()


class AuthContextMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        LogContext.set_from_message(event)

        try:
            if not event.text:
                return await handler(event, data)

            command = event.text.split()[0].lower()
            user_id = event.from_user.id if event.from_user else None

            public_commands = {"/start", "/idgrupo", "/owner", "/getid", "/adminhelp"}
            allowed_commands = {"/d", "/getsong"}
            admin_commands = {"/allowuser", "/removeuser", "/getuseradmins", "/getbotusers"}
            owner_commands = {"/allowadmin", "/removeadmin", "/clearcache"}

            if command in public_commands:
                return await handler(event, data)

            is_owner = user_id and user_id == int(OWNER_ID)
            is_admin = is_owner or (user_id and user_handler.is_admin(user_id))

            if command in owner_commands and not is_owner:
                await event.reply("No tienes permisos para realizar esta accion")
                logger.warning("Permission denied (owner only)", user_id=user_id)
                return

            if command in admin_commands and not is_admin:
                await event.reply("No tienes permisos para realizar esta accion")
                logger.warning("Permission denied (admin only)", user_id=user_id)
                return

            if command in allowed_commands:
                is_allowed = is_admin or (user_id and user_handler.is_user_allowed(user_id))
                if not is_allowed:
                    await event.reply(
                        "You cant use this function, please contact an admin of the bot"
                    )
                    logger.warning("Permission denied (not allowed)", user_id=user_id)
                    return
                return await handler(event, data)

            if not command.startswith("/") and event.chat.type == "private":
                if re.search(r"https?://[^\s]+", event.text):
                    is_allowed = is_admin or (user_id and user_handler.is_user_allowed(user_id))
                    if not is_allowed:
                        await event.reply(
                            "You cant use this function, please contact an admin of the bot"
                        )
                        logger.warning("Permission denied (not allowed)", user_id=user_id)
                        return
                    return await handler(event, data)

            return await handler(event, data)

        finally:
            LogContext.clear()