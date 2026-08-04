from contextvars import ContextVar
from dataclasses import dataclass, field, asdict
from typing import Optional

from aiogram.types import Message

from utils.url_utils import sanitize_url


@dataclass
class RequestContext:
    user_id: Optional[int] = None
    username: Optional[str] = None
    command: Optional[str] = None
    chat_id: Optional[int] = None
    chat_type: Optional[str] = None
    media_url: Optional[str] = None
    media_format: Optional[str] = None
    duration: Optional[int] = None


_context: ContextVar[RequestContext] = ContextVar("request_context", default=RequestContext())


class LogContext:

    @staticmethod
    def set_from_message(message: Message):
        first_token = message.text.split()[0] if message.text else None
        command = sanitize_url(first_token) if first_token else None
        ctx = RequestContext(
            user_id=message.from_user.id if message.from_user else None,
            username=message.from_user.username if message.from_user else None,
            command=command,
            chat_id=message.chat.id,
            chat_type=message.chat.type,
        )
        _context.set(ctx)

    @staticmethod
    def set_media_metadata(url: str, duration: Optional[int], media_format: str):
        ctx = _context.get()
        ctx.media_url = url
        ctx.duration = duration
        ctx.media_format = media_format
        _context.set(ctx)

    @staticmethod
    def get() -> RequestContext:
        return _context.get()

    @staticmethod
    def clear():
        _context.set(RequestContext())


def log_context_patcher(record):
    ctx = _context.get()
    for key, value in asdict(ctx).items():
        if value is not None:
            record["extra"][key] = value