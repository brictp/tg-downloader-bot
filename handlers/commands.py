from utils.user_allowed_handler import UserHandler

from handlers.mixins.info import InfoMixin
from handlers.mixins.download import DownloadMixin
from handlers.mixins.admin import AdminMixin


class BotHandlers(InfoMixin, DownloadMixin, AdminMixin):
    def __init__(self):
        self.user_handler = UserHandler()