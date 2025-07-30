import requests
from typing import Dict, Any
from ..domain.notification import Notification

class NtfyClient:
    def __init__(self, endpoint: str, default_headers: Dict[str, Any]):
        self.endpoint = endpoint
        self.default_headers = {k: str(v) for k, v in default_headers.items()}

    def send(self, notif: Notification):
        headers = self.default_headers.copy()
        if notif.title:
            headers["Title"] = notif.title
        if notif.headers:
            headers.update({k: str(v) for k, v in notif.headers.items()})
        resp = requests.post(self.endpoint, data=notif.message.encode('utf-8'), headers=headers)
        resp.raise_for_status()
        return resp.status_code