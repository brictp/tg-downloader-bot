import os
import yt_dlp

from utils.enums import MediaFormat


def get_download_options(format_message: MediaFormat) -> dict:
    if format_message == MediaFormat.MP3:
        return {
            "outtmpl": "./media/%(title)s.%(ext)s",
            "format": "bestaudio[filesize<20M]/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "wav",
                    "preferredquality": "0",
                }
            ],
            "noplaylist": True,
        }
    elif format_message == MediaFormat.MP4:
        return {
            "outtmpl": "./media/%(title)s.%(ext)s",
            "format": "mp4/bestvideo[filesize<20M]+bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegVideoConvertor",
                    "preferedformat": "mp4",
                }
            ],
        }
    else:
        raise ValueError(f"Formato no soportado: {format_message}")


def download_media(url: str, format_message: MediaFormat) -> str:
    options = get_download_options(format_message)

    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=True)

        final_path = info["requested_downloads"][0]["filepath"]

    if not os.path.exists(final_path):
        return "File not found"

    file_size = os.path.getsize(final_path) / (1024 * 1024)  # en MB
    if file_size > 20:
        os.remove(final_path)
        return "Archivo demasiado grande, se ha eliminado."

    return final_path
