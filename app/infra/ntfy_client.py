import logging
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from typing import Dict, Any
from ..domain.notification import Notification

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class NtfyClient:
    def __init__(self, endpoint: str, default_headers: Dict[str, Any]):
        self.endpoint = endpoint
        self.default_headers = {k: str(v) for k, v in default_headers.items()}
        
        # Set up retries
        retries = Retry(
            total=5,
            backoff_factor=1,
            status_forcelist=[502, 503, 504],
            allowed_methods=["POST"]  # Use 'allowed_methods' instead of 'method_whitelist'
        )
        adapter = HTTPAdapter(max_retries=retries)
        self.session = requests.Session()
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def send(self, notif: Notification):
        headers = self.default_headers.copy()
        if notif.title:
            headers["Title"] = notif.title
        if notif.headers:
            headers.update({k: str(v) for k, v in notif.headers.items()})
        
        try:
            logger.debug(f"Attempting to send notification to {self.endpoint}")
            response = self.session.post(
                self.endpoint,
                data=notif.message.encode("utf-8"),
                headers=headers
            )
            response.raise_for_status()
            logger.info(f"Notification sent successfully: {response.status_code}")
            return response.status_code
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send notification: {e}")
            return None