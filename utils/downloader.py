from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

from utils.enums import MediaFormat
from handlers.downlaod_config_factory import DownloadConfigFactory


def download_media(url: str, format_message: MediaFormat) -> str:
    try:
        options = DownloadConfigFactory.get_config(format_message)

        with YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=True)

        final_path = info["requested_downloads"][0]["filepath"]

    except DownloadError as e:
        raise RuntimeError(f"failed to download media {e}")

    return final_path
