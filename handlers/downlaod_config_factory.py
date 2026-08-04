from typing import Dict

from utils.enums import MediaFormat
from utils.logger import YtDlpLogBridge


class DownloadConfigFactory:
    MEDIA_DIR = "./media/%(title)s.%(ext)s"

    @staticmethod
    def get_config(format_type: MediaFormat) -> Dict:
        base_config = {
            "outtmpl": DownloadConfigFactory.MEDIA_DIR,
            "noplaylist": True,
            "noprogress": True,
            "logger": YtDlpLogBridge(),
        }

        if format_type == MediaFormat.MP3:
            return {
                **base_config,
                "format": "bestaudio/best",
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "wav",
                        "preferredquality": "0",
                    }
                ],
            }

        elif format_type == MediaFormat.MP4:
            return {
                **base_config,
                "format": "bestvideo+bestaudio/best",
                "merge_output_format": "mp4",
                "postprocessors": [
                    {
                        "key": "FFmpegVideoConvertor",
                        "preferedformat": "mp4",
                    }
                ],
            }

        elif format_type == MediaFormat.BEST:
            return {
                **base_config,
                "format": "best",
            }

        else:
            raise ValueError(f"Unsupported format: {format_type}")
