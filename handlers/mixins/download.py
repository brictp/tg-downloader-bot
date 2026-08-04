import asyncio

from aiogram.types import Message, FSInputFile, ReactionTypeEmoji

from config.settings import CHANNEL_ID

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
from utils.size_validator import extract_info, validate_media_size
from utils.url_utils import canonical_key_from_url, cache_key_from_info, sanitize_url
from utils.cache import VideoCache


class DownloadMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cache = VideoCache()
        self._download_locks: dict[str, asyncio.Lock] = {}

    @property
    def _cache_enabled(self) -> bool:
        return CHANNEL_ID != 0

    def _get_lock(self, cache_key: str) -> asyncio.Lock:
        lock = self._download_locks.get(cache_key)
        if lock is None:
            lock = asyncio.Lock()
            self._download_locks[cache_key] = lock
        return lock

    def _drop_lock(self, cache_key: str):
        self._download_locks.pop(cache_key, None)

    async def _copy_cached(self, message: Message, cache_key: str, message_id: int):
        await message.bot.copy_message(
            chat_id=message.chat.id,
            from_chat_id=CHANNEL_ID,
            message_id=message_id,
        )
        logger.info("Video sent from cache", cache_key=cache_key)

    async def search_and_download(self, message: Message):
        url, _time_to_short = get_params_from_message(message.text)

        if url is None:
            return

        cache_key = None
        if self._cache_enabled:
            cache_key = canonical_key_from_url(url)
            if cache_key:
                message_id = self.cache.get(cache_key)
                if message_id:
                    await self._copy_cached(message, cache_key, message_id)
                    return

        title = None
        try:
            info = extract_info(url, MediaFormat.MP4)
            title = info.get("title")

            ok, error_msg = validate_media_size(info, MediaFormat.MP4)
            if not ok:
                await message.reply(error_msg)
                return

            if cache_key is None and self._cache_enabled:
                cache_key = cache_key_from_info(info)
                if cache_key:
                    message_id = self.cache.get(cache_key)
                    if message_id:
                        await self._copy_cached(message, cache_key, message_id)
                        return
        except Exception as e:
            logger.exception("Failed to extract media info")

        await message.react([ReactionTypeEmoji(emoji="💯")])

        if cache_key:
            lock = self._get_lock(cache_key)
            async with lock:
                try:
                    message_id = self.cache.get(cache_key)
                    if message_id:
                        await self._copy_cached(message, cache_key, message_id)
                        return
                    await self._download_to_channel(message, url, cache_key, title)
                finally:
                    self._drop_lock(cache_key)
        else:
            await self._download_to_channel(message, url, cache_key, title)

    async def _download_to_channel(
        self,
        message: Message,
        url: str,
        cache_key: str | None,
        title: str | None,
    ):
        path_to_video = None

        try:
            path_to_video = download_media(url, MediaFormat.MP4)
            video_file = FSInputFile(path_to_video)

            clean_url = sanitize_url(url)
            caption = clean_url
            if title:
                caption = f"{title}\n{clean_url}"

            if self._cache_enabled and cache_key:
                posted = await message.bot.send_video(
                    chat_id=CHANNEL_ID,
                    video=video_file,
                    caption=caption,
                )
                self.cache.set(cache_key, posted.message_id)
                await message.bot.copy_message(
                    chat_id=message.chat.id,
                    from_chat_id=CHANNEL_ID,
                    message_id=posted.message_id,
                )
            else:
                await message.bot.send_video(
                    chat_id=message.chat.id,
                    video=video_file,
                    caption=caption,
                )

            logger.info("Video sent successfully", cache_key=cache_key)

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

            info = extract_info(url, MediaFormat.MP3)
            ok, error_msg = validate_media_size(info, MediaFormat.MP3)
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
