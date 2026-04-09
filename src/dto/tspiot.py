from dataclasses import dataclass
from typing import Optional


@dataclass
class TSPIoTRequestRegistration:
    id: str  # идентификатор инстанса ЕСМ
    kktSerial: str  # Серийный номер кассы
    fnSerial: str  # Серийный номер ФН
    kktInn: str  # ИНН на который зарегистрирована касса


@dataclass
class TSPIoTRegistrationResponse:
    """ Структура-результат выполнения запроса создания сервиса ESM """
    success: bool = False
    tspiot_id: Optional[str] = None
    status: Optional[str] = None
    error_message: Optional[str] = None



@dataclass
class TSPIoTRequestCreateInstance:
    kkt_serial: str  # идентификатор инстанса ЕСМ заполняется значением kktSerial из списка ДККТ
    port: int | None = None  # порт для подключения оркестратора
    softPort: int | None = None  # ПОРТ ДЛЯ ПМСР


@dataclass
class TspiotCreateInstanceResult:
    """Результат создания ESM сервиса"""
    success: bool = False
    tspiot_id: Optional[str] = None
    status: Optional[str] = None  # "Создан", "Уже существует"
    error_message: Optional[str] = None
    error_code: Optional[int] = None  # для кода ошибки из API



@dataclass
class ESM:
    #url 1.2.3 -> 'http://127.0.0.1:51077/api/v1/instances/info/0128245621'

    logPath: str #путь к логам
    state: str
    clientPort: int
    version: str
    licenses: list[str]
    isActive: bool
    activeTill: str
    lastSync: str
    regData: str #пока неизвестно что там придёт
    tspiotId: str
    gismtTspiotId: str
    kktSerial: str
    fnSerial: str
    kktInn: str
    espToken: str