from dataclasses import dataclass
from typing import Optional, List
import httpx

from src.core.config import ApiSettings
from src.network.base import ApiClient


# DTO для сетевого слоя
@dataclass
class GisMtSettingsResponseDTO:
    """DTO для ответа с настройками драйвера ГИС МТ"""
    compatibilityMode: bool
    allowRemoteConnection: bool
    gismtAddress: str

    @classmethod
    def from_dict(cls, data: dict) -> 'GisMtSettingsResponseDTO':
        return cls(
            compatibilityMode=data.get('compatibilityMode', False),
            allowRemoteConnection=data.get('allowRemoteConnection', False),
            gismtAddress=data.get('gismtAddress', '')
        )


@dataclass
class GisMtSettingsUpdateDTO:
    """DTO для обновления настроек драйвера ГИС МТ"""
    compatibilityMode: Optional[bool] = None
    allowRemoteConnection: Optional[bool] = None
    gismtAddress: Optional[str] = None

    def to_dict(self) -> dict:
        result = {}
        if self.compatibilityMode is not None:
            result['compatibilityMode'] = self.compatibilityMode
        if self.allowRemoteConnection is not None:
            result['allowRemoteConnection'] = self.allowRemoteConnection
        if self.gismtAddress is not None:
            result['gismtAddress'] = self.gismtAddress
        return result


@dataclass
class InstanceResponseDTO:
    """DTO для информации об инстансе"""
    id: str
    serviceState: str
    port: int
    createdAt: Optional[str] = None


@dataclass
class InstancesListResponseDTO:
    """DTO для списка инстансов"""
    instances: List[InstanceResponseDTO]

    @classmethod
    def from_dict(cls, data: dict) -> 'InstancesListResponseDTO':
        instances = []
        for inst in data.get('instances', []):
            instances.append(InstanceResponseDTO(
                id=inst.get('id', ''),
                serviceState=inst.get('serviceState', ''),
                port=inst.get('port', 0),
                createdAt=inst.get('createdAt')
            ))
        return cls(instances=instances)


class GisMtNetwork(ApiClient):
    """
    Сетевой слой для работы с ГИС МТ
    Только реальные запросы к API, без тестовых данных
    """

    __INSTANCES_URL = "/api/v1/instances"
    __SETTINGS_URL = "/api/v1/settings"

    def __init__(self):
        super().__init__()
        self._client = None
        self.config = ApiSettings()

    def _get_client(self) -> httpx.Client:
        """Получает или создает HTTPX клиент"""
        if self._client is None or self._client.is_closed:
            self._client = httpx.Client(
                base_url=self.config.orchestrator_url,
                timeout=30.0
            )
        return self._client

    def get_instances(self) -> Optional[InstancesListResponseDTO]:
        """
        Получает список всех инстансов
        GET /api/v1/instances
        """
        try:
            client = self._get_client()
            response = client.get(self.__INSTANCES_URL)

            if response.status_code == 200:
                data = response.json()
                return InstancesListResponseDTO.from_dict(data)
            else:
                print(f"❌ Ошибка получения инстансов: {response.status_code}")
                return None

        except Exception as e:
            print(f"❌ Ошибка в get_instances: {e}")
            return None

    def get_settings(self, instance_id: str) -> Optional[GisMtSettingsResponseDTO]:
        """
        Получает настройки драйвера ГИС МТ для указанного инстанса
        GET /api/v1/settings/{id}
        """
        try:
            client = self._get_client()
            url = f"{self.__SETTINGS_URL}/{instance_id}"
            response = client.get(url)

            if response.status_code == 200:
                data = response.json()
                return GisMtSettingsResponseDTO.from_dict(data)
            elif response.status_code == 404:
                print(f"ℹ️ Инстанс {instance_id} не найден")
                return None
            else:
                print(f"❌ Ошибка получения настроек: {response.status_code}")
                return None

        except Exception as e:
            print(f"❌ Ошибка в get_settings: {e}")
            return None

    def update_settings(self, instance_id: str, settings: GisMtSettingsUpdateDTO) -> bool:
        """
        Обновляет настройки драйвера ГИС МТ
        PUT /api/v1/settings/{id}
        """
        try:
            client = self._get_client()
            url = f"{self.__SETTINGS_URL}/{instance_id}"
            payload = settings.to_dict()

            response = client.put(url, json=payload)

            if response.status_code in [200, 201, 204]:
                return True
            else:
                print(f"❌ Ошибка обновления настроек: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ Ошибка в update_settings: {e}")
            return False

    def close(self):
        """Закрывает клиент"""
        if self._client and not self._client.is_closed:
            self._client.close()

    def __del__(self):
        self.close()

