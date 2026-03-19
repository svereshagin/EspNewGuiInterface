from dataclasses import dataclass
import httpx
from typing import Optional, Dict, Any

from src.core.config import ApiSettings
from src.network.base import ApiClient





@dataclass
class RequestGetInfoRegime:
    esm_instance_id: str

@dataclass
class ResponseGetSettingsRegime:
    address: str
    port: int
    login: str
    password: str

@dataclass
class OsInfo:
    JKpINWX4KaNP: str  # windows
    UO6QA5RdY: str     # информация о версии Windows
    I2VTPQ3M0VW: str   # amd64


@dataclass
class Databases:
    blocked_cis: Dict[str, Any]
    blocked_gtin: Dict[str, Any]
    min_price: Dict[str, Any]


@dataclass
class DbState:
    databases: Databases


@dataclass
class LmStatus:
    dbState: DbState
    dbVersion: str
    inn: str
    inst: str
    lastSync: int
    lastUpdate: int
    name: str
    operationMode: str
    serviceUrl: str
    status: str
    version: str


@dataclass
class ResponseGetInfoRegime:
    controllerVersion: str
    code: int
    osInfo: OsInfo
    lmStatus: LmStatus


# Функция для преобразования словаря в датакласс
def dict_to_response_get_info_regime(data: dict) -> ResponseGetInfoRegime:
    return ResponseGetInfoRegime(
        controllerVersion=data['controllerVersion'],
        code=data['code'],
        osInfo=OsInfo(
            JKpINWX4KaNP=data['osInfo']['JKpINWX4KaNP'],
            UO6QA5RdY=data['osInfo']['UO6QA5RdY'],
            I2VTPQ3M0VW=data['osInfo']['I2VTPQ3M0VW']
        ),
        lmStatus=LmStatus(
            dbState=DbState(
                databases=Databases(
                    blocked_cis=data['lmStatus']['dbState']['databases']['blocked_cis'],
                    blocked_gtin=data['lmStatus']['dbState']['databases']['blocked_gtin'],
                    min_price=data['lmStatus']['dbState']['databases']['min_price']
                )
            ),
            dbVersion=data['lmStatus']['dbVersion'],
            inn=data['lmStatus']['inn'],
            inst=data['lmStatus']['inst'],
            lastSync=data['lmStatus']['lastSync'],
            lastUpdate=data['lmStatus']['lastUpdate'],
            name=data['lmStatus']['name'],
            operationMode=data['lmStatus']['operationMode'],
            serviceUrl=data['lmStatus']['serviceUrl'],
            status=data['lmStatus']['status'],
            version=data['lmStatus']['version']
        )
    )

@dataclass
class RequestSetupRegime:
    esm_instance_id: str
    address: str
    port: int
    login: str
    password: str

    def to_dict(self) -> dict:
        return {
            'address': self.address,
            'port': self.port,
            'login': self.login,
            'password': self.password
        }


class RegimeNetwork(ApiClient):
    __GET_LM_CZ_INFO = "/api/v1/instances/lm/"
    __SETUP_LC_CZ = "/api/v1/settings/lm/"

    config = ApiSettings()

    def __init__(self):
        super().__init__()
        self._client = None

    def _get_client(self):
        if self._client is None or self._client.is_closed:
            base_url = self.config.orchestrator_url
            self._client = httpx.Client(
                base_url=base_url,
                timeout=30.0,
                verify=False
            )
        return self._client

    def get_regime_settings_by_instance(self, data: RequestGetInfoRegime):
        """
        Для получения настроек, которые применил юзер
        IP, PORT, LOGIN, PASSWORD
        """
        try:
            client = self._get_client()
            response = client.get(self.__SETUP_LC_CZ+data.esm_instance_id)
            data = response.json()
            return ResponseGetSettingsRegime(address=data['address'], port=data['port'], login=data['login'], password=data['password'])
        except httpx.HTTPError as e:
            print(e)


    def get_regime_config_by_instance(self, data: RequestGetInfoRegime) -> Optional[ResponseGetInfoRegime]:
        try:
            client = self._get_client()
            response = client.get(self.__GET_LM_CZ_INFO + data.esm_instance_id)
            response_data = response.json()
            return dict_to_response_get_info_regime(response_data)
        except httpx.HTTPError as e:
            print(e)
            return None

    def setup_regime_settings(self, data: RequestSetupRegime):
        payload = data.to_dict()
        print(payload)
        try:
            # ИСПРАВЛЕНИЕ: используем _get_client() вместо with ApiClient()
            client = self._get_client()
            response = client.put(
                self.__SETUP_LC_CZ + data.esm_instance_id,
                json=payload
            )
            if response.status_code == 200:
                print("Настройки для instance ESM with ID", data.esm_instance_id, "were changed successfully")
            return response
        except httpx.HTTPError as e:
            print(e)
            return None

    def close(self):
        if self._client and not self._client.is_closed:
            self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


regimeNetwork = RegimeNetwork()

# Использование без контекстного менеджера
regimeNetwork.setup_regime_settings(
    RequestSetupRegime(
        esm_instance_id="00106327428745",
        address="127.0.0.1",
        port=50063,
        login="admin",
        password="admin"
    )
)

regimeNetwork.get_regime_config_by_instance(
    RequestGetInfoRegime(esm_instance_id="00106327428745")
)

response = regimeNetwork.get_regime_settings_by_instance(
    RequestGetInfoRegime(esm_instance_id="00106327428745")
)
print(response)