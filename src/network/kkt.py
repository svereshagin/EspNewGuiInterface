import httpx
from typing import Optional
import asyncio
from contextlib import asynccontextmanager

from src.domain.kkt.entity import CashInfo
from src.core.config import ApiSettings
from src.domain.common.regime_local_module import KktInfo
from src.network.base import ApiClient


class KKTNetwork(ApiClient):
    __DKKT_URL = "/api/v1/dkktList"
    __SETTINGS_LM_URL = "/api/v1/settings/lm"
    config = ApiSettings()

    # Конфигурация таймаутов
    CONNECTION_TIMEOUT = 10.0
    READ_TIMEOUT = 30.0
    KEEPALIVE_TIMEOUT = 60.0
    MAX_KEEPALIVE_CONNECTIONS = 10

    # Переменная класса для синглтона
    _instance = None
    _lock = asyncio.Lock()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        super().__init__()
        self._client: Optional[httpx.AsyncClient] = None
        self._client_lock = asyncio.Lock()
        self._request_lock = asyncio.Lock()  # Блокировка для запросов
        self._last_request_time = 0
        self._initialized = True
        print(f"✅ KKTNetwork синглтон инициализирован с базовым URL: {self.config.orchestrator_url}")

    async def _get_client(self) -> httpx.AsyncClient:
        """
        Получает или создает HTTPX клиент с правильной конфигурацией
        """
        async with self._client_lock:
            if self._client is None or self._client.is_closed:
                limits = httpx.Limits(
                    max_keepalive_connections=self.MAX_KEEPALIVE_CONNECTIONS,
                    max_connections=20,
                    keepalive_expiry=self.KEEPALIVE_TIMEOUT
                )

                timeout = httpx.Timeout(self.READ_TIMEOUT)

                self._client = httpx.AsyncClient(
                    base_url=self.config.orchestrator_url,
                    timeout=timeout,
                    limits=limits,
                    follow_redirects=True,
                    max_redirects=5,
                    verify=False
                )
                print("✅ Создан новый Async HTTPX клиент")

            return self._client

    async def get_dkktList(self) -> Optional[CashInfo]:
        """
        Асинхронное получение списка касс с правильной обработкой таймаутов
        """
        # Блокируем параллельные запросы
        async with self._request_lock:
            print("🔍 Запрос к /api/v1/dkktList")

            try:
                client = await self._get_client()

                # Добавляем retry логику
                for attempt in range(3):
                    try:
                        response = await client.get(
                            self.__DKKT_URL,
                            timeout=self.READ_TIMEOUT
                        )

                        print(f"📥 Статус: {response.status_code} (попытка {attempt + 1})")

                        if response.status_code == 200:
                            data = response.json()
                            cash_info = CashInfo.from_api_response(data)
                            print(f"✅ Данные получены: {len(cash_info.kkt)} касс")
                            return cash_info
                        elif response.status_code in [502, 503, 504]:
                            print(f"⚠️ Временная ошибка, повтор через {2 ** attempt}с")
                            await asyncio.sleep(2 ** attempt)
                            continue
                        else:
                            print(f"❌ Ошибка API: {response.status_code}")
                            return None

                    except httpx.TimeoutException as e:
                        print(f"⏱️ Таймаут (попытка {attempt + 1})")
                        if attempt < 2:
                            await asyncio.sleep(2 ** attempt)
                            continue
                        return None

                    except httpx.NetworkError as e:
                        print(f"🌐 Сетевая ошибка (попытка {attempt + 1})")
                        if attempt < 2:
                            await asyncio.sleep(2 ** attempt)
                            continue
                        return None

            except Exception as e:
                print(f"❌ Ошибка: {e}")
                return None

    async def close(self):
        """Асинхронное закрытие клиента"""
        async with self._client_lock:
            if self._client and not self._client.is_closed:
                await self._client.aclose()
                self._client = None
                print("🔒 HTTPX клиент закрыт")

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()