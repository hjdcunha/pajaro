import json
from pathlib import Path
from typing import Any, Dict

class AppConfig:
    def __init__(self, path: str = "config.json"):
        raw = json.loads(Path(path).read_text())
        self.ntfy_url: str = raw["ntfy_url"].rstrip("/")
        self.topic: str = raw["topic"]
        self.title: str = raw.get("default_title", "")
        self.headers: Dict[str, Any] = raw.get("headers", {})

    def endpoint(self) -> str:
        return f"{self.ntfy_url}/{self.topic}"
