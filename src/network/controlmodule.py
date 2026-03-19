import httpx
from typing import Optional, List
from dataclasses import dataclass
from src.core.config import ApiSettings
from src.network.base import ApiClient


@dataclass
class ComponentStatusDTO:
    """Статус соединения для отдельного компонента системы"""
    code: int
    error: str
    lastConnection: str  # формат: "15:32:33 19-03-2026"


@dataclass
class ClientSoftwareStatusDTO(ComponentStatusDTO):
    """Статус клиентского ПО (расширенный)"""
    name: str
    version: str
    id: str


@dataclass
class SystemsStatusResponseDTO:
    """
    Ответ на запрос статуса соединений системы
    GET /api/v1/status/{id}
    """
    gismt: ComponentStatusDTO
    lmController: ComponentStatusDTO
    lm: ComponentStatusDTO
    lmInternet: ComponentStatusDTO
    lmServers: ComponentStatusDTO
    esp: ComponentStatusDTO
    clientSoftware: ClientSoftwareStatusDTO

    @property
    def gismt_status(self) -> str:
        """Удобное свойство для получения текстового статуса ГИС МТ"""
        if self.gismt.code == 0:
            return "Подключено"
        elif self.gismt.code == 1:
            return f"Ошибка: {self.gismt.error}"
        else:
            return f"Неизвестный статус (код {self.gismt.code})"

    @property
    def all_systems_ok(self) -> bool:
        """Проверка, что все системы работают (code = 0)"""
        systems = [
            self.gismt,
            self.lmController,
            self.lm,
            self.lmInternet,
            self.lmServers,
            self.esp
        ]
        return all(system.code == 0 for system in systems)


def parse_status_response(data: dict) -> SystemsStatusResponseDTO:
    """Парсит JSON ответ в DTO объект"""
    client_software = ClientSoftwareStatusDTO(
        code=data["clientSoftware"]["code"],
        error=data["clientSoftware"]["error"],
        lastConnection=data["clientSoftware"]["lastConnection"],
        name=data["clientSoftware"]["name"],
        version=data["clientSoftware"]["version"],
        id=data["clientSoftware"]["id"]
    )

    return SystemsStatusResponseDTO(
        gismt=ComponentStatusDTO(
            code=data["gismt"]["code"],
            error=data["gismt"]["error"],
            lastConnection=data["gismt"]["lastConnection"]
        ),
        lmController=ComponentStatusDTO(
            code=data["lmController"]["code"],
            error=data["lmController"]["error"],
            lastConnection=data["lmController"]["lastConnection"]
        ),
        lm=ComponentStatusDTO(
            code=data["lm"]["code"],
            error=data["lm"]["error"],
            lastConnection=data["lm"]["lastConnection"]
        ),
        lmInternet=ComponentStatusDTO(
            code=data["lmInternet"]["code"],
            error=data["lmInternet"]["error"],
            lastConnection=data["lmInternet"]["lastConnection"]
        ),
        lmServers=ComponentStatusDTO(
            code=data["lmServers"]["code"],
            error=data["lmServers"]["error"],
            lastConnection=data["lmServers"]["lastConnection"]
        ),
        esp=ComponentStatusDTO(
            code=data["esp"]["code"],
            error=data["esp"]["error"],
            lastConnection=data["esp"]["lastConnection"]
        ),
        clientSoftware=client_software
    )


@dataclass
class LicenseInfo:
    """Информация о лицензии"""
    licenses: List[dict]
    isActive: bool
    activeTill: str
    lastSync: str


@dataclass
class RegistrationData:
    """Регистрационные данные"""
    tspiotId: str
    gismtTspiotId: str
    kktSerial: str
    fnSerial: str
    kktInn: str
    espToken: str


@dataclass
class Controlmodule_instance_info_DTO:
    """DTO для информации о состоянии контрольного модуля"""
    logPath: str
    state: str
    clientPort: int
    version: str
    licenseInfo: LicenseInfo
    regData: RegistrationData


@dataclass
class Controlmodule_info_DTO:
    app_path: str
    version: str
    log_path: str


@dataclass
class Controlmodule_instance_DTO:
    id: str
    port: int
    serviceState: str  # Работает/Остановлено


@dataclass
class Controlmodule_instances_DTO:
    instances: list[Controlmodule_instance_DTO]


class ControlmoduleNetwork(ApiClient):
    __CONTROLMODULE_INFO_URL = "/api/v1/info"
    __CONTROLMODULE_INSTANCES = "/api/v1/instances/info"
    __CONTROLMODULE_INSTANCE_INFO = "/api/v1/instances/info/"  # instance_id
    __CONTROLMODULE_ALL_SYSTEMS_STATUS = "/api/v1/status/"  # все статусы

    config = ApiSettings()

    def __init__(self):
        super().__init__()
        self._client = None

    def get_systems_status(self, instance_id: str) -> Optional[SystemsStatusResponseDTO]:
        """
        Получает статус соединений всех систем для указанного экземпляра
        GET /api/v1/status/{id}
        """
        try:
            client = self._get_client()
            url = f"{self.__CONTROLMODULE_ALL_SYSTEMS_STATUS}{instance_id}"

            print(f"📥 Запрос статуса систем для экземпляра: {instance_id}")
            response = client.get(url)

            if response.status_code == 200:
                data = response.json()
                print(f"✅ Статус систем получен")

                status_dto = parse_status_response(data)

                print(f"   ГИС МТ: код {status_dto.gismt.code} - {status_dto.gismt_status}")
                print(f"   ЛМ: код {status_dto.lm.code}")
                print(f"   Все системы OK: {status_dto.all_systems_ok}")

                return status_dto
            else:
                print(f"❌ Ошибка получения статуса: {response.status_code}")
                return None

        except Exception as e:
            print(f"❌ Ошибка в get_systems_status: {e}")
            return None

    def _get_client(self):
        """Получает или создает HTTPX клиент"""
        if self._client is None or self._client.is_closed:
            self._client = httpx.Client(
                base_url=self.config.orchestrator_url,
                timeout=30.0
            )
            print("✅ Создан новый HTTPX клиент")
        return self._client

    def _get_cm_info(self) -> Optional[Controlmodule_info_DTO]:
        """Получает общую информацию о драйвере"""
        try:
            client = self._get_client()
            response = client.get(self.__CONTROLMODULE_INFO_URL)
            print(f"Статус GET info: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                dto = Controlmodule_info_DTO(
                    app_path=data["appPath"],
                    version=data["version"],
                    log_path=data["logPath"]
                )
                print(f"✅ Версия драйвера: {dto.version}")
                return dto
            else:
                print(f"❌ Ошибка API: статус {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Ошибка в _get_cm_info: {e}")
            return None

    def _get_cm_instances(self) -> Optional[Controlmodule_instances_DTO]:
        """
        Получает список зарегистрированных экземпляров ТС ПИоТ
        """
        try:
            client = self._get_client()
            response = client.get(self.__CONTROLMODULE_INSTANCES)
            print(f"📥 Статус GET {self.__CONTROLMODULE_INSTANCES}: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                instances_list = []
                for inst_data in data.get("instances", []):
                    instance = Controlmodule_instance_DTO(
                        id=inst_data["id"],
                        port=inst_data["port"],
                        serviceState=inst_data["serviceState"]
                    )
                    instances_list.append(instance)

                print(f"📦 Найдено экземпляров: {len(instances_list)}")
                return Controlmodule_instances_DTO(instances=instances_list)

            elif response.status_code == 204:
                print("ℹ️ Нет зарегистрированных экземпляров")
                return Controlmodule_instances_DTO(instances=[])

            else:
                print(f"❌ Ошибка API: статус {response.status_code}")
                return None

        except Exception as e:
            print(f"❌ Ошибка в _get_cm_instances: {e}")
            return None

    def _get_cm_instance_info(self, esm_instance_id: str) -> Optional[Controlmodule_instance_info_DTO]:
        """
        Получает детальную информацию о конкретном экземпляре ЕСМ
        GET /api/v1/instances/info/{id}
        """
        try:
            client = self._get_client()
            url = f"{self.__CONTROLMODULE_INSTANCE_INFO}{esm_instance_id}"

            print(f"📥 Запрос детальной информации для экземпляра: {esm_instance_id}")
            response = client.get(url)

            if response.status_code == 200:
                data = response.json()
                print(f"✅ Получена информация для экземпляра {esm_instance_id}")

                # Парсим лицензии
                licenses_data = data.get("licenses", [])
                license_info = LicenseInfo(
                    licenses=licenses_data,
                    isActive=licenses_data[0].get("isActive", False) if licenses_data else False,
                    activeTill=licenses_data[0].get("activeTill", "") if licenses_data else "",
                    lastSync=licenses_data[0].get("lastSync", "") if licenses_data else ""
                )

                # Парсим регистрационные данные
                reg_data = data.get("regData", {})
                registration_data = RegistrationData(
                    tspiotId=reg_data.get("tspiotId", ""),
                    gismtTspiotId=reg_data.get("gismtTspiotId", ""),
                    kktSerial=reg_data.get("kktSerial", ""),
                    fnSerial=reg_data.get("fnSerial", ""),
                    kktInn=reg_data.get("kktInn", ""),
                    espToken=reg_data.get("espToken", "")
                )

                # Создаем DTO
                instance_info = Controlmodule_instance_info_DTO(
                    logPath=data.get("logPath", ""),
                    state=data.get("state", ""),
                    clientPort=data.get("clientPort", 0),
                    version=data.get("version", ""),
                    licenseInfo=license_info,
                    regData=registration_data
                )

                print(f"   Состояние: {instance_info.state}")
                print(f"   Версия: {instance_info.version}")

                return instance_info
            else:
                print(f"❌ Ошибка получения информации: {response.status_code}")
                return None

        except Exception as e:
            print(f"❌ Ошибка в _get_cm_instance_info: {e}")
            return None


# # ВЫЗОВ МЕТОДА ДЛЯ ИНСТАНСА 00106327428745
# if __name__ == "__main__":
#     import time
#
#     print("=" * 60)
#     print("🚀 Тестирование ControlmoduleNetwork")
#     print("=" * 60)
#
#     # Создаем экземпляр класса
#     network = ControlmoduleNetwork()
#
#     # ID инстанса для проверки
#     INSTANCE_ID = "00106327428745"
#
#     print(f"\n🔍 Проверка статуса систем для инстанса: {INSTANCE_ID}")
#     print("-" * 40)
#
#     # Получаем статус систем
#     status = network.get_systems_status(INSTANCE_ID)
#
#     if status:
#         print("\n✅ Результат получения статуса:")
#         print(f"   ГИС МТ: {status.gismt_status}")
#         print(f"   Последнее соединение с ГИС МТ: {status.gismt.lastConnection}")
#         print(f"   Статус ЛМ: код {status.lm.code}")
#         print(f"   Статус ESP: код {status.esp.code}")
#         print(f"   Клиентское ПО: {status.clientSoftware.name} v{status.clientSoftware.version}")
#         print(f"   Все системы работают: {status.all_systems_ok}")
#     else:
#         print(f"❌ Не удалось получить статус для инстанса {INSTANCE_ID}")
#
#     print("\n" + "=" * 60)