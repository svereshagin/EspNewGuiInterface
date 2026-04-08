from dataclasses import dataclass
from enum import Enum
from typing import List


class ServiceState(str, Enum):
    """Состояние сервиса"""
    STOPPED = "Остановлено"
    WAITING_START = "Ожидает запуска"
    WAITING_STOP = "Ожидает остановки"
    RUNNING = "Работает"
    WAITING_RESUME = "Ожидает продолжения"
    WAITING_PAUSE = "Ожидает паузы"
    PAUSED = "Приостановлено"
    REBOOTING = "Перезагрузка"
    ERROR = "Ошибка"
    UNKNOWN = "Неизвестно"


@dataclass
class ControlModuleInfo:
    #Запрос GET на endpoint /api/v1/info
    app_path: str = ''#Путь к Controlmodule/Оркестратору
    version: str = '' #Версия ESM
    log_path: str = ' '#Путь к логам


@dataclass
class InstanceESMInfo:
    instance_id: str
    port: str
    service_state: ServiceState


@dataclass
class InstancesESM:
    """
    1.2.2.	Запрос получения списка запущенных ЕСМ 'http://127.0.0.1:51077/api/v1/instances/info'
    """
    instances: List[InstanceESMInfo]

