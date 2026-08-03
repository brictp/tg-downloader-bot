from aiogram.types import Message, FSInputFile, ReactionTypeEmoji

from utils import (
    download_media,
    delete_file,
    get_params_from_message,
    logger,
)

from utils.get_song_name import (
    audio_converter,
    request_to_shazam,
    parse_shazam_response,
)

from utils.enums import MediaFormat
from utils.size_validator import validate_media_size
from config.settings import MAX_FILE_SIZE_VIDEO, MAX_FILE_SIZE_AUDIO


class DownloadMixin:
    async def search_and_download(self, message: Message):
        url, _time_to_short = get_params_from_message(message.text)

        if url is None:
            return

        ok, error_msg = validate_media_size(url, MediaFormat.MP4)
        if not ok:
            await message.reply(error_msg)
            return

        await message.react([ReactionTypeEmoji(emoji="💯")])
        path_to_video = None

        try:
            path_to_video = download_media(url, MediaFormat.MP4)

            video_file = FSInputFile(path_to_video)
            await message.bot.send_video(
                chat_id=message.chat.id,
                video=video_file,
            )
            logger.info("Video sent successfully")

        except Exception as e:
            await message.reply("Error al enviar el video")
            logger.exception("Failed to send video")

        finally:
            if path_to_video:
                await delete_file(path_to_video)

    async def get_song_name(self, message: Message):
        path_to_media = None

        try:
            url, time_to_short = get_params_from_message(message.text)

            ok, error_msg = validate_media_size(url, MediaFormat.MP3)
            if not ok:
                await message.reply(error_msg)
                return

            await message.react([ReactionTypeEmoji(emoji="💯")])
            path_to_media = download_media(url, MediaFormat.MP3)
            logger.info("Audio downloaded for Shazam")

            audio_converted = audio_converter(path_to_media, time_to_short)
            res = request_to_shazam(audio_converted)
            song_name = parse_shazam_response(res)

            await message.reply(song_name)

        except Exception as e:
            await message.reply("Error al procesar la solicitud")
            logger.exception("Failed to process song request")

        if path_to_media:
            await delete_file(path_to_media)