from utils.enums import MediaFormat
from typing import Dict


class DownloadConfigFactory:
    MEDIA_DIR = "./media/%(title)s.%(ext)s"

    @staticmethod
    def get_config(format_type: MediaFormat) -> Dict:
        base_config = {
            "outtmpl": DownloadConfigFactory.MEDIA_DIR,
            "noplaylist": True,
        }

        if format_type == MediaFormat.MP3:
            return {
                **base_config,
                "format": "bestaudio/best",
                "max-filesize": "6M",
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
                "max-filesize": "15M",
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
