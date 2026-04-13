# dto/TSPIOT.qml.py
from dataclasses import dataclass
from enum import Enum
from typing import Optional, List



# ==================== SERVICE DTO ====================
@dataclass
class TSPIoTRegistrationServiceResult:
    is_registered: bool = False
    message: str = ""
    counter: int = 0






# ==================== БАЗОВЫЕ DTO ====================

@dataclass
class TSPIoTRequestRegistration:
    id: str
    kktSerial: str
    fnSerial: str
    kktInn: str


@dataclass
class TSPIoTRegistrationResponse:
    success: bool = False
    tspiot_id: Optional[str] = None
    status: Optional[str] = None
    error_message: Optional[str] = None


@dataclass
class TSPIoTRequestCreateInstance:
    kkt_serial: str
    port: int | None = None
    softPort: int | None = None


@dataclass
class TspiotCreateInstanceResult:
    success: bool = False
    tspiot_id: Optional[str] = None
    status: Optional[str] = None
    error_message: Optional[str] = None
    error_code: Optional[int] = None


# ==================== СТАТУСЫ СИСТЕМ ====================

@dataclass
class TSPIoTComponentStatusDTO:
    code: int
    error: str
    lastConnection: str


@dataclass
class TSPIoTClientSoftwareStatusDTO(TSPIoTComponentStatusDTO):
    name: str
    version: str
    id: str


@dataclass
class TSPIoTSystemsStatusResponseDTO:
    gismt: TSPIoTComponentStatusDTO
    lmController: TSPIoTComponentStatusDTO
    lm: TSPIoTComponentStatusDTO
    lmInternet: TSPIoTComponentStatusDTO
    lmServers: TSPIoTComponentStatusDTO
    esp: TSPIoTComponentStatusDTO
    clientSoftware: TSPIoTClientSoftwareStatusDTO

    @property
    def gismt_status(self) -> str:
        if self.gismt.code == 0:
            return "Подключено"
        elif self.gismt.code == 1:
            return f"Ошибка: {self.gismt.error}"
        else:
            return f"Неизвестный статус (код {self.gismt.code})"

    @property
    def all_systems_ok(self) -> bool:
        systems = [
            self.gismt, self.lmController, self.lm,
            self.lmInternet, self.lmServers, self.esp
        ]
        return all(system.code == 0 for system in systems)


# ==================== ИНФОРМАЦИЯ ОБ ИНСТАНСЕ ====================

@dataclass
class TSPIoTLicenseInfo:
    """Информация о лицензии"""
    isActive: bool
    activeTill: str
    lastSync: str


@dataclass
class TSPIoTRegistrationData:
    """Регистрационные данные TSPIoT"""
    tspiotId: str
    gismtTspiotId: str
    kktSerial: str
    fnSerial: str
    kktInn: str
    espToken: str


@dataclass
class TSPIoTInstanceInfoDTO:
    """DTO для информации о состоянии инстанса TSPIoT (1.2.3)"""
    logPath: str
    state: str
    clientPort: int
    version: str
    licenses: List[TSPIoTLicenseInfo]  # список лицензий
    regData: TSPIoTRegistrationData

    @property
    def is_registered(self) -> bool:
        """Проверка, зарегистрирован ли инстанс"""
        return self.state == "Зарегистрирован"

    @property
    def has_active_license(self) -> bool:
        """Проверка, есть ли активная лицензия"""
        for license_info in self.licenses:
            if license_info.isActive:
                return True
        return False

    @property
    def tspiot_id(self) -> str:
        """Удобное свойство для получения tspiotId"""
        return self.regData.tspiotId


# ==================== СПИСОК ИНСТАНСОВ ====================

class ServiceState(str, Enum):
    """Состояние сервиса ЕСМ"""
    STOPPED = "Остановлено"
    WAITING_START = "Ожидает запуска"
    WAITING_STOP = "Ожидает остановки"
    RUNNING = "Работает"
    WAITING_CONTINUE = "Ожидает продолжения"
    WAITING_PAUSE = "Ожидает паузы"
    PAUSED = "Приостановлено"
    REBOOT = "Перезагрузка"
    ERROR = "Ошибка"
    UNKNOWN = "Неизвестно"


@dataclass
class TSPIoTInstanceDTO:
    """DTO для информации об инстансе в списке (1.2.2)"""
    id: str
    port: int
    serviceState: str

    @property
    def is_running(self) -> bool:
        return self.serviceState == ServiceState.RUNNING

    @property
    def is_stopped(self) -> bool:
        return self.serviceState == ServiceState.STOPPED

    @property
    def has_error(self) -> bool:
        return self.serviceState == ServiceState.ERROR


@dataclass
class TSPIoTInstancesResponseDTO:
    """Ответ на запрос списка запущенных ЕСМ (1.2.2)"""
    instances: List[TSPIoTInstanceDTO]

    @property
    def count(self) -> int:
        return len(self.instances)

    @property
    def running_instances(self) -> List[TSPIoTInstanceDTO]:
        return [inst for inst in self.instances if inst.is_running]

    @property
    def stopped_instances(self) -> List[TSPIoTInstanceDTO]:
        return [inst for inst in self.instances if inst.is_stopped]

    @property
    def first_instance(self) -> Optional[TSPIoTInstanceDTO]:
        return self.instances[0] if self.instances else None

    def get_instance_by_id(self, instance_id: str) -> Optional[TSPIoTInstanceDTO]:
        for inst in self.instances:
            if inst.id == instance_id:
                return inst
        return None