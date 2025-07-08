import re
from aiogram.types import Message, FSInputFile


from utils import (
    download_media,
    register_error,
    delete_file,
    identify_song_from_file,
)

from utils.enums import MediaFormat


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
                "🔄 Downloading, this may take a few moments..."
            )

            try:
                # Descargar el video
                path_to_video = download_media(url, MediaFormat.MP4)

                # Subir el video al grupo de Telegram
                video_file = FSInputFile(path_to_video)
                await message.bot.send_video(
                    chat_id=message.chat.id,
                    video=video_file,
                    caption="🎥 Heres ur video.",
                )

                if status_message:
                    await status_message.delete()

                await delete_file(path_to_video)

            except Exception as e:
                await message.reply("Error downloading video.")
                register_error(e)

                if status_message:
                    await status_message.delete()

    async def get_song_name(self, message: Message):
        """Buscar URL en mensaje y descargar video"""
        url_pattern = r"https?://[^\s]+"
        urls = re.findall(url_pattern, message.text)

        if not urls:
            message.reply("Error to find media")
            return

        url = urls[0]
        status_message = await message.reply("Wait a minute, Looking for media....")
        print(url)

        try:
            # Download audio
            path_to_media = download_media(url, MediaFormat.MP3)

            song_name = await identify_song_from_file(path_to_media)

            await message.reply(song_name)

            if status_message:
                await status_message.delete()
            await delete_file(path_to_media)

        except Exception as e:
            await message.reply("Error downloading video")
            print(f"error: {e}")
            register_error(e)
            if status_message:
                await status_message.delete()
