from aiogram.types import Message


async def validate_user_id(message: Message, user_id):
    try:
        user_id = int(user_id)
        return user_id
    except Exception as e:
        await message.reply("El id debe ser un numero valido")
        return False
