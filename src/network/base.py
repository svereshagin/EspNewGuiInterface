import logging
from typing import Optional, Dict
import httpx
from src.core.config import ApiSettings

logger = logging.getLogger(__name__)


class ApiClient:
    """Базовый HTTP клиент"""

    def __init__(self):
        self.config = ApiSettings()

        self.client = httpx.Client(
            base_url=self.config.orchestrator_url,
            timeout=self.config.timeout,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": "ESM-GUI/1.0",
            },
            limits=httpx.Limits(
                max_keepalive_connections=5,
                max_connections=10,
            ),
        )

    def close(self):
        if hasattr(self, "client") and not self.client.is_closed:
            self.client.close()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()

    def get(self, endpoint: str, params: Optional[Dict] = None, timeout: Optional[float] = None) -> httpx.Response:
        return self.client.get(endpoint, params=params, timeout=timeout)

    def post(self, endpoint: str, data: Optional[Dict] = None, timeout: Optional[float] = None) -> httpx.Response:
        return self.client.post(endpoint, json=data, timeout=timeout)

    def put(self, endpoint: str, data: Optional[Dict] = None, timeout: Optional[float] = None) -> httpx.Response:
        return self.client.put(endpoint, json=data, timeout=timeout)

    def delete(self, endpoint: str, timeout: Optional[float] = None) -> httpx.Response:
        return self.client.delete(endpoint, timeout=timeout)

    def patch(self, endpoint: str, data: Optional[Dict] = None, timeout: Optional[float] = None) -> httpx.Response:
        return self.client.patch(endpoint, json=data, timeout=timeout)