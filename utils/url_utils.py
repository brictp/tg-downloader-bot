import re

_YOUTUBE_ID_RE = re.compile(r"(?:v=|/shorts/|/embed/|/live/|/v/|youtu\.be/)([\w-]{6,})")


def canonical_key_from_url(url: str) -> str | None:
    match = _YOUTUBE_ID_RE.search(url)
    if match:
        return f"youtube:{match.group(1)}"
    return None


def cache_key_from_info(info: dict) -> str | None:
    extractor = info.get("extractor")
    video_id = info.get("id")
    if extractor and video_id:
        return f"{extractor}:{video_id}"
    return None


def sanitize_url(url: str) -> str:
    key = canonical_key_from_url(url)
    if key and key.startswith("youtube:"):
        return f"https://youtu.be/{key.split(':', 1)[1]}"

    base = url.split("?", 1)[0].split("#", 1)[0]
    return base
