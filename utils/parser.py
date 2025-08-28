import re


def get_params_from_message(text: str) -> tuple[str | None, int | None]:
    try:
        # Extract valid url
        url_pattern = r"https?://[^\s]+"
        urls = re.findall(url_pattern, text)
        url = urls[0] if urls else None

        if url is None:
            return None, None

        # Find valid timestamp
        parts = text.strip().split()
        timestamp = None

        for part in parts:
            if part == url or part.startswith("/"):
                continue
            if is_timestamp_format(part):
                timestamp = parse_timestamp_to_ms(part)
                break

        return url, timestamp

    except Exception as e:
        raise ValueError(f"Error parsing message: {e}")


def is_timestamp_format(s: str) -> bool:
    return bool(re.match(r"^\d{1,2}(:\d{1,2}){1,2}$", s.strip()))


def parse_timestamp_to_ms(timestamp: str) -> int:
    """
    Convert string type 'MM:SS' or 'HH:MM:SS' to miliseconds
    Valid examples: '1:34', '00:01:34', '01:02:03'
    """
    parts = timestamp.strip().split(":")
    if not 1 <= len(parts) <= 3:
        raise ValueError(f"Valid Format: '{timestamp}'")

    parts = [int(p) for p in parts]
    while len(parts) < 3:
        parts.insert(0, 0)

    hours, minutes, seconds = parts
    total_ms = (hours * 3600 + minutes * 60 + seconds) * 1000
    return total_ms
