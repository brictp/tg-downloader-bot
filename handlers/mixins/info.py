from aiogram.types import Message

from utils import logger
from config.settings import OWNER_ID


class InfoMixin:
    async def start_bot(self, message: Message):
        owner_id = int(OWNER_ID)
        owner_link = f"<a href='tg://user?id={owner_id}'>Owner</a>"
        text = (
            f"Bienvenido al bot descargador 🚀\n\n"
            f"Comandos:\n"
            f"<b>/d</b> &lt;url&gt; — Descargar video (en grupos)\n"
            f"<b>/getsong</b> &lt;url&gt; — 🔴 No disponible\n"
            f"<b>/getid</b> — Obtener tu ID\n"
            f"<b>/owner</b> — Info del creador\n\n"
            f"En privado solo envía una URL y descargo automáticamente.\n"
            f"Creado por {owner_link}"
        )
        await message.reply(text, parse_mode="HTML")
        logger.info("Bot started")

    async def get_owner(self, message: Message):
        owner_id = int(OWNER_ID)
        link = f"tg://user?id={owner_id}"
        try:
            chat = await message.bot.get_chat(owner_id)
            name = chat.full_name or chat.username or f"ID: {owner_id}"
        except Exception:
            name = f"ID: {owner_id}"
        await message.reply(
            f"Owner del bot: <a href='{link}'>{name}</a>",
            parse_mode="HTML",
        )
        logger.info("Owner info requested")

    async def get_user_id(self, message: Message):
        user_id = message.from_user.id
        await message.reply(
            f"Tu ID es: <code>{user_id}</code>",
            parse_mode="HTML",
        )
        logger.info("User ID requested")

    async def get_group_id(self, message: Message):
        if message.chat.type in ("group", "supergroup"):
            chat_id = message.chat.id
            await message.reply(f"Group id: {chat_id}")
            logger.info("Group ID requested", group_id=chat_id)
        elif message.chat.type == "private":
            await message.reply("This command only works in groups")
            logger.info("Group ID command used in private chat")
        else:
            await message.reply("Cannot determine the type of chat")

    async def admin_help(self, message: Message):
        user_id = message.from_user.id
        is_owner = user_id == int(OWNER_ID)
        is_admin = is_owner or self.user_handler.is_admin(user_id)

        if not is_admin:
            await message.reply("No tienes permisos para ver esto")
            logger.warning("Admin help blocked", user_id=user_id)
            return

        text = (
            "Comandos de administración:\n\n"
            "/allowuser <id> — Permitir usuario\n"
            "/removeuser <id> — Remover usuario\n"
            "/allowadmin <id> — Promover admin\n"
            "/removeadmin <id> — Remover admin\n"
            "/idgrupo — Obtener ID del grupo\n"
            "/getuseradmins — Listar administradores\n"
            "/getbotusers — Listar usuarios permitidos\n"
            "/adminhelp — Mostrar esta ayuda"
        )
        await message.reply(text)
        logger.info("Admin help shown", user_id=user_id)