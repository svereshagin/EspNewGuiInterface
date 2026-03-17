import httpx
from typing import Optional

from domain.kkt.entity import CashInfo
from src.core.config import ApiSettings
from src.domain.common.regime_local_module import KktInfo
from src.network.base import ApiClient
from dataclasses import dataclass

from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime



@dataclass
class LicenseInfo:
    """Информация о лицензии"""
    licenses: List[dict]  # информация о лицензии (массив объектов)
    isActive: bool  # активна лицензия или нет
    activeTill: str  # срок действия лицензии (дата формата Go)
    lastSync: str  # время последней проверки лицензии (дата формата Go)

@dataclass
class RegistrationData:
    """Регистрационные данные"""
    tspiotId: str  # идентификатор ТС ПИоТ
    gismtTspiotId: str  # идентификатор в ГИС МТ
    kktSerial: str  # серийный номер кассы
    fnSerial: str  # серийный номер ФН
    kktInn: str  # ИНН на который зарегистрирована касса
    espToken: str  # токен в системе ЕСП

@dataclass
class Controlmodule_instance_info_DTO:
    """DTO для информации о состоянии контрольного модуля"""
    logPath: str  # путь к лог файлам
    state: str  # статус регистрации
    clientPort: int  # порт для подключения ПМСР (сервис проверки КМ)
    version: str  # версия ЕСМ
    licenseInfo: LicenseInfo  # информация о лицензии
    regData: RegistrationData  # регистрационные данные


@dataclass
class Controlmodule_info_DTO:
    app_path: str
    version: str
    log_path: str

@dataclass
class Controlmodule_instance_DTO:
    id: str
    port: int
    serviceState: str #Работает/Остановлено
    # {"instances": [{"id": "0128245621", "port": 50401, "serviceState": "Работает"}]}
    # {"instances": [{"id": "00106329566391", "port": 50401, "serviceState": "Остановлено"}]}


@dataclass
class Controlmodule_instalces_DTO:
    instances: list[Controlmodule_instance_DTO]



class ControlmoduleNetwork(ApiClient):
    __CONTROLMODULE_INFO_URL = "/api/v1/info"
    __CONTROLMODULE_INSTANCES = "/api/v1/instances/info"
    __CONTROLMODULE_INSTANCE_INFO = "/api/v1/instances/info/" #instance_id


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

    def _get_cm_info(self):
        try:
            client = self._get_client()
            response = client.get(self.__CONTROLMODULE_INFO_URL)
            print(f"Статус: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                dto = Controlmodule_info_DTO(data["appPath"], data["version"], data["logPath"])
                return dto
            else:
                print(f"Ошибка API: статус {response.status_code}")
                print(f"Ответ: {response.text}")
                return None
        except Exception as e:
            print(e)

    def _get_cm_instances(self):
        try:
            client = self._get_client()
            response = client.get(self.__CONTROLMODULE_INSTANCES)
            print(f"Статус: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                dto = Controlmodule_info_DTO(data["appPath"], data["version"], data["logPath"])
                return dto
            if response.status_code == 204:
                #TODO видимо это значит, что у нас нет зареганных экземпляров тспиот
                return None
            else:
                print(f"Ошибка API: статус {response.status_code}")
                print(f"Ответ: {response.text}")
                return None
        except Exception as e:
            print(e)

    def _get_cm_instance_info(self, esm_instance_id: str):
        try:
            client = self._get_client()
            response = client.get(self.__CONTROLMODULE_INSTANCE_INFO + instance_id)
        except Exception as e:
            print(e)




cm = ControlmoduleNetwork()



# Запрос GET на endpoint /api/v1/info
# Пример запроса:
# curl --location 'http://127.0.0.1:51077/api/v1/info'
#
# Примеры ответа:
# {"appPath":"/opt/esp/esm/bin/controlmodule","version":"1.4.5.7","logPath":"/var/log/esp/esm/um"}
#
# {"appPath":"C:\\Program Files\\ESP\\ESM\\bin\\controlmodule.exe","version":"1.4.5.7","logPath":"C:\\ProgramData\\esp\\esm\\um\\log"}
# Поля ответа:
# Параметр	Тип	Описание
# appPath	string	путь до binary оркестратора
# version	string	версия оркестратора
# logPath	string	путь к логам
