import os

from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

from utils.enums import MediaFormat


def download_media(url: str, format_message: MediaFormat) -> str:
    from utils.logger import logger
    from utils.log_context import LogContext
    from handlers.downlaod_config_factory import DownloadConfigFactory

    try:
        options = DownloadConfigFactory.get_config(format_message)
        fmt = format_message.value

        logger.info("Download started", media_url=url, format=fmt)

        with YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=True)

        final_path = info["requested_downloads"][0]["filepath"]
        duration = info.get("duration")
        file_size = os.path.getsize(final_path)

        LogContext.set_media_metadata(url, duration, fmt)
        logger.info("Download complete", media_url=url, duration=duration, format=fmt, file_size=file_size)

    except DownloadError as e:
        logger.exception("Download failed", media_url=url, format=format_message.value)
        raise RuntimeError(f"failed to download media {e}")

    return final_path