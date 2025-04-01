import re
from aiogram.types import Message, FSInputFile

from utils import download_video, register_error, delete_video


class BotHandlers:
    def __init__(self):
        """Inicializa la clase con la instancia del bot"""

    async def start_bot(self, message: Message):
        """Comando /start"""
        print("hello i started")
        await message.reply("hellow")

    async def get_group_id(self, message: Message):
        """Obtener ID del grupo"""
        print("hello i started idgrupo")

        if message.chat.type in ("group", "supergroup"):
            chat_id = message.chat.id
            await message.reply(f"Group id: {chat_id}")
        elif message.chat.type == "private":
            await message.reply("This command only works in groups")
        else:
            await message.reply("Cannot determine the type of chat")

    async def search_and_download(self, message: Message):
        """Buscar URL en mensaje y descargar video"""
        url_pattern = r"https?://[^\s]+"
        urls = re.findall(url_pattern, message.text)

        if urls:
            url = urls[0]
            status_message = await message.reply(
                "🔄 Descargando el video, esto puede tardar unos momentos..."
            )

            try:
                # Descargar el video
                path_to_video = download_video(url)

                # Subir el video al grupo de Telegram
                video_file = FSInputFile(path_to_video)
                await message.bot.send_video(
                    chat_id=message.chat.id,
                    video=video_file,
                    caption="🎥 Aquí está tu video.",
                )

                delete_video(path_to_video)

            except Exception as e:
                await message.reply("Error descargando video")
                print(f"error: {e}")
                register_error(e)

            await status_message.delete()
