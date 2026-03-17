
import httpx
from typing import Optional

from domain.kkt.entity import CashInfo
from src.core.config import ApiSettings
from src.domain.common.regime_local_module import KktInfo
from src.network.base import ApiClient


class KKTNetwork(ApiClient):
    __GET_LM_CZ_INFO = "/api/v1/instances/lm/" #+id
    config = ApiSettings()

    def __init__(self):
        super().__init__()
        self._client = None  # Сохраняем клиент для повторного использования

    def _get_client(self):
        """Получает или создает HTTPX клиент"""
        if self._client is None or self._client.is_closed:
            # Создаем клиент без контекстного менеджера
            self._client = httpx.Client(
                base_url=self.config.orchestrator_url,
                timeout=30.0
            )
            print("✅ Создан новый HTTPX клиент")
        return self._client

    def _get_regime_info(self, esm_instance_id: str):
        client = self._get_client()
        response = client.get(self.__GET_LM_CZ_INFO+esm_instance_id)

