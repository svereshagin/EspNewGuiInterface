from dataclasses import dataclass
from typing import Optional, Dict
import httpx

from src.core.config import ApiSettings


class ApiClient:
    """Базовый HTTP клиент (синглтон с поддержкой контекстного менеджера)"""

    _instance: Optional['ApiClient'] = None
    _initialized: bool = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """
        Инициализация клиента

        Args:
            config: Настройки API (всегда передается)
        """
        if self._initialized:
            return

        self.config = ApiSettings()

        # Базовые заголовки
        base_headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "ESM-GUI/1.0",
        }

        self.client = httpx.Client(
            base_url=self.config.orchestrator_url,
            timeout=self.config.timeout,
            headers=base_headers,
            limits=httpx.Limits(
                max_keepalive_connections=5,
                max_connections=10
            )
        )

        self._initialized = True
        print(f"ApiClient инициализирован с базовым URL: {self.config.orchestrator_url}")

    # === Контекстный менеджер ===

    def __enter__(self):
        """Вход в контекстный менеджер"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Выход из контекстного менеджера - гарантированно закрываем соединения"""
        self.close()

    # === Методы для работы с клиентом ===

    def close(self):
        """Закрыть клиент и освободить ресурсы"""
        if hasattr(self, 'client'):
            self.client.close()
            print("ApiClient закрыт")

    def get(self, endpoint: str, params: Optional[Dict] = None) -> httpx.Response:
        """GET запрос"""
        return self.client.get(endpoint, params=params)

    def post(self, endpoint: str, data: Optional[Dict] = None) -> httpx.Response:
        """POST запрос"""
        return self.client.post(endpoint, json=data)

    def put(self, endpoint: str, data: Optional[Dict] = None) -> httpx.Response:
        """PUT запрос"""
        return self.client.put(endpoint, json=data)

    def delete(self, endpoint: str) -> httpx.Response:
        """DELETE запрос"""
        return self.client.delete(endpoint)

    def patch(self, endpoint: str, data: Optional[Dict] = None) -> httpx.Response:
        """PATCH запрос"""
        return self.client.patch(endpoint, json=data)

    # === Деструктор ===

    def __del__(self):
        """Деструктор для гарантии закрытия"""
        self.close()
