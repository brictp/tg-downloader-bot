import time
from typing import Callable, Dict, Any, Awaitable

from aiogram.types import Message
from aiogram import BaseMiddleware

from utils import logger
from config.settings import RATE_LIMIT_SECONDS, OWNER_ID


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, rate_limit: int = RATE_LIMIT_SECONDS):
        self.rate_limit = rate_limit
        self.user_last_called: Dict[int, float] = {}

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        if not event.from_user:
            return await handler(event, data)

        user_id = event.from_user.id

        heavy_commands = {"/d", "/getsong"}
        is_heavy = False
        if event.text:
            command = event.text.split()[0].lower()
            if command in heavy_commands:
                is_heavy = True
        if not is_heavy and event.chat.type == "private" and event.text:
            import re
            if re.search(r"https?://[^\s]+", event.text):
                is_heavy = True

        if not is_heavy:
            return await handler(event, data)

        if user_id == int(OWNER_ID):
            return await handler(event, data)

        now = time.time()
        last = self.user_last_called.get(user_id, 0)
        elapsed = now - last

        if elapsed < self.rate_limit:
            remaining = int(self.rate_limit - elapsed)
            await event.reply(f"⏳ Esperá {remaining} segundos antes de hacer otra solicitud")
            logger.warning("Rate limit exceeded", user_id=user_id, remaining=remaining)
            return

        self.user_last_called[user_id] = now
        return await handler(event, data)