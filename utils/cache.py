import json

from config.settings import VIDEO_CACHE_FILE

from utils.logger import logger


class VideoCache:
    def __init__(self):
        self.data: dict[str, int] = self._load_data()

    def _load_data(self) -> dict[str, int]:
        default_data: dict[str, int] = {}

        if not VIDEO_CACHE_FILE.exists():
            return default_data

        with open(VIDEO_CACHE_FILE, "r") as f:
            try:
                loaded = json.load(f)
                return loaded if isinstance(loaded, dict) else default_data
            except json.JSONDecodeError:
                logger.warning("Cache file corrupted, starting empty", path=str(VIDEO_CACHE_FILE))
                return default_data

    def _save_data(self):
        VIDEO_CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(VIDEO_CACHE_FILE, "w") as f:
            json.dump(self.data, f, indent=2)

    def get(self, cache_key: str) -> int | None:
        return self.data.get(cache_key)

    def set(self, cache_key: str, message_id: int):
        self.data[cache_key] = message_id
        self._save_data()

    def remove(self, cache_key: str):
        if cache_key in self.data:
            del self.data[cache_key]
            self._save_data()

    def clear(self):
        self.data.clear()
        self._save_data()
