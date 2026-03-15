from dataclasses import dataclass
from enum import Enum
from typing import List


class ShiftState(str, Enum):
    """Состояние смены"""
    CLOSED = "Закрыта"
    OPENED = "Открыта"
    EXPIRED = "Истекла"


@dataclass
class KktInfo:
    """Информация о конкретной кассе"""
    kktSerial: str  # серийный номер кассы
    fnSerial: str  # серийный номер ФН
    kktInn: str  # ИНН на который зарегистрирована касса
    kktRnm: str  # регистрационный номер ККТ
    modelName: str  # наименование модели кассы
    dkktVersion: str  # версия ДККТ
    developer: str  # разработчик ДККТ
    manufacturer: str  # производитель кассы
    shiftState: ShiftState  # состояние смены

@dataclass
class CashInfo:
    """Информация о подключенных кассах"""
    kkt: List[KktInfo]  # список подключенных касс

