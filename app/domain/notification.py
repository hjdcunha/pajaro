from dataclasses import dataclass
from typing import Optional, Dict

@dataclass
class Notification:
    message: str
    title: Optional[str] = None
    headers: Optional[Dict[str, str]] = None