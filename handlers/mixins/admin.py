from aiogram.types import Message

from utils import logger
from utils.helper_handler import resolve_user_identifier


class AdminMixin:
    async def add_user(self, message: Message):
        raw = await self.get_id_from_message(message)
        if not raw:
            return

        user_id = await resolve_user_identifier(message.bot, raw)
        if not user_id:
            await message.reply("Usuario no encontrado")
            return

        self.user_handler.add_user(user_id)
        await message.reply("Usuario agregado")
        logger.info("User added by admin", target_user_id=user_id)

    async def remove_user(self, message: Message):
        raw = await self.get_id_from_message(message)
        if not raw:
            return

        user_id = await resolve_user_identifier(message.bot, raw)
        if not user_id:
            await message.reply("Usuario no encontrado")
            return

        await self.user_handler.remove_user(user_id)
        await message.reply("Usuario eliminado")
        logger.info("User removed by admin", target_user_id=user_id)

    async def add_admin(self, message: Message):
        raw = await self.get_id_from_message(message)
        if not raw:
            return

        user_id = await resolve_user_identifier(message.bot, raw)
        if not user_id:
            await message.reply("Usuario no encontrado")
            return

        self.user_handler.add_admin(int(user_id))
        await message.reply("Usuario agregado a administracion")
        logger.info("Admin added by owner", target_user_id=user_id)

    async def delete_admin(self, message: Message):
        raw = await self.get_id_from_message(message)
        if not raw:
            return

        user_id = await resolve_user_identifier(message.bot, raw)
        if not user_id:
            await message.reply("Usuario no encontrado")
            return

        await self.user_handler.remove_admin(int(user_id))
        await message.reply("Usuario eliminado de administracion")
        logger.info("Admin removed by owner", target_user_id=user_id)

    async def list_admins(self, message: Message):
        admins = self.user_handler.list_admins()
        if not admins:
            await message.reply("No hay administradores registrados")
            return
        text = "**Administradores:**\n" + "\n".join(f"• `{uid}`" for uid in admins)
        await message.reply(text)

    async def list_users(self, message: Message):
        users = self.user_handler.list_users()
        if not users:
            await message.reply("No hay usuarios permitidos")
            return
        text = "**Usuarios permitidos:**\n" + "\n".join(f"• `{uid}`" for uid in users)
        await message.reply(text)

    async def get_id_from_message(self, message: Message):
        parts = message.text.split()
        if len(parts) < 2:
            await message.reply("Debes especificar un ID de usuario")
            return
        return parts[1]