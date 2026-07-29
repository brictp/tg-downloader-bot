from aiogram.types import Message


async def validate_user_id(message: Message, user_id):
    try:
        user_id = int(user_id)
        return user_id
    except Exception as e:
        await message.reply("El id debe ser un numero valido")
        return False


async def resolve_user_identifier(bot, identifier: str) -> int | None:
    raw = identifier.strip().lstrip("@")
    if raw.isdigit():
        return int(raw)
    try:
        chat = await bot.get_chat(f"@{raw}")
        return chat.id
    except Exception:
        return None