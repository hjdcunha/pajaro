from ..config import AppConfig
from ..domain.notification import Notification
from ..infra.ntfy_client import NtfyClient

class SendNotificationUseCase:
    def __init__(self, cfg: AppConfig):
        self.cfg = cfg
        self.client = NtfyClient(cfg.endpoint(), cfg.headers)

    def execute(self, message: str, title: str = None, extra_headers: dict = None):
        notif = Notification(
            message=message,
            title=title or self.cfg.title,
            headers=extra_headers or {}
        )
        status = self.client.send(notif)
        return status