from aiogram.types import Message, FSInputFile


from utils import (
    download_media,
    register_error,
    delete_file,
    get_params_from_message,
)

from utils.user_allowed_handler import UserHandler

from utils.get_song_name import (
    audio_converter,
    request_to_shazam,
    parse_shazam_response,
)

from utils.enums import MediaFormat


class BotHandlers:
    def __init__(self):
        """Inicializa la clase con la instancia del bot"""
        self.user_handler = UserHandler()

    async def start_bot(self, message: Message):
        """Comando /start"""
        await message.reply("hellow")

    async def get_group_id(self, message: Message):
        """Obtener ID del grupo"""

        if message.chat.type in ("group", "supergroup"):
            chat_id = message.chat.id
            await message.reply(f"Group id: {chat_id}")
        elif message.chat.type == "private":
            await message.reply("This command only works in groups")
        else:
            await message.reply("Cannot determine the type of chat")

    async def search_and_download(self, message: Message):
        """Buscar URL en mensaje y descargar video"""

        if not self.user_handler.is_user_allowed(message.from_user.id):
            await message.reply(
                "You cant use this function, please contact an admin of the bot"
            )
            return

        url, _time_to_short = get_params_from_message(message.text)

        if url is None:
            return

        status_message = await message.reply(
            "🔄 Downloading, this may take a few moments..."
        )

        try:
            path_to_video = download_media(url, MediaFormat.MP4)

            video_file = FSInputFile(path_to_video)
            await message.bot.send_video(
                chat_id=message.chat.id,
                video=video_file,
            )

        except Exception as e:
            await message.reply("Error Sending video")
            register_error(e)

        finally:
            if status_message:
                await status_message.delete()

            await delete_file(path_to_video)

    async def get_song_name(self, message: Message):
        """Search for the name of a song from a video or audio file"""
        path_to_media = None
        try:
            url, time_to_short = get_params_from_message(message.text)
            status_message = await message.reply("Wait a minute, Looking for media....")
            path_to_media = download_media(url, MediaFormat.MP3)

            audio_converted = audio_converter(path_to_media, time_to_short)
            res = request_to_shazam(audio_converted)
            song_name = parse_shazam_response(res)

            await message.reply(song_name)

        except Exception as e:
            await message.reply("Error downloading video")
            register_error(e)

        await status_message.delete()
        await delete_file(path_to_media)

    async def add_user(self, message: Message):
        await self.is_admin(message)

        user_id = self.get_id_from_message(message)
        await self.user_handler.add_user(int(user_id))
        return

    async def remove_user(self, message: Message):
        await self.is_admin(message)

        user_id = self.get_id_from_message(message)
        print(user_id)
        await self.user_handler.remove_user(int(user_id))
        await message.reply("Usuario eliminado de administracion")
        return

    async def add_admin(self, message: Message):
        await self.is_admin(message)
        admin_user_id = 7646859427
        if message.from_user.id != admin_user_id:
            message.reply("No tienes permiso para eliminar administradores")

        user_id = self.get_id_from_message(message)
        await self.user_handler.add_admin(int(user_id))
        await message.reply("Usuario agregado a administracion")
        return

    async def delete_admin(self, message: Message):
        await self.is_admin(message)
        admin_user_id = 7646859427
        if message.from_user.id != admin_user_id:
            message.reply("No tienes permiso para eliminar administradores")

        user_id = self.get_id_from_message(message)
        print(user_id)
        await self.user_handler.remove_admin(int(user_id))
        await message.reply("Usuario eliminado de administracion")
        return

    def get_id_from_message(self, message: Message):
        return message.text.split(" ")[1]

    async def is_admin(self, message: Message):
        if not self.user_handler.is_admin(message.from_user.id):
            await message.reply("Solo un admin puede autorizar usuarios.")
            return
