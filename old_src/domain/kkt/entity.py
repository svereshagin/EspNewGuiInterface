from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Dict, Any
import json


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

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'KktInfo':
        """Создание объекта из словаря (ответа API)"""
        # Очищаем поля от лишних пробелов
        cleaned_data = {
            'kktSerial': data.get('kktSerial', '').strip(),
            'fnSerial': data.get('fnSerial', '').strip(),
            'kktInn': data.get('kktInn', '').strip(),
            'kktRnm': data.get('kktRnm', '').strip(),
            'modelName': data.get('modelName', '').strip(),
            'dkktVersion': data.get('dkktVersion', '').strip(),
            'developer': data.get('developer', '').strip(),
            'manufacturer': data.get('manufacturer', '').strip(),
            'shiftState': ShiftState(data.get('shiftState', 'Закрыта').strip())
        }
        return cls(**cleaned_data)

    def __str__(self) -> str:
        """Строковое представление для отладки"""
        return f"ККТ {self.modelName} (№{self.kktSerial}), смена: {self.shiftState.value}"


@dataclass
class CashInfo:
    """Информация о подключенных кассах"""
    # url -> 'http://127.0.0.1:51077/api/v1/dkktList'
    kkt: List[KktInfo] = field(default_factory=list)  # список подключенных касс

    @classmethod
    def from_api_response(cls, response_data: Dict[str, Any]) -> 'CashInfo':
        """Создание объекта из ответа API"""
        kkt_list = []

        # Проверяем структуру ответа
        if 'kkt' in response_data and isinstance(response_data['kkt'], list):
            for kkt_item in response_data['kkt']:
                try:
                    kkt_info = KktInfo.from_dict(kkt_item)
                    kkt_list.append(kkt_info)
                except (KeyError, ValueError) as e:
                    print(f"Ошибка парсинга кассы: {e}, данные: {kkt_item}")
                    continue

        return cls(kkt=kkt_list)

    def __len__(self) -> int:
        """Количество касс"""
        return len(self.kkt)

    def __getitem__(self, index: int) -> KktInfo:
        """Доступ по индексу"""
        return self.kkt[index]

    #==============================Business Logic====================================
    @classmethod
    def get_all_cash_with_same_inn(cls, inn: str) -> List[KktInfo]:
        """
        Возвращает все только те обьекты касс, где один и тот же ИНН
        """
        kkt_array: list[KktInfo] = []

        for kkt in cls.kkt:
            if kkt.kktInn == inn:
                kkt_array.append(kkt)
        return kkt_array


    def get_serial_numbers(self) -> List[str]:
        """Получить список серийных номеров всех касс"""
        return [kkt.kktSerial for kkt in self.kkt]

    def find_by_serial(self, serial: str) -> Optional[KktInfo]:
        """Найти кассу по серийному номеру"""
        for kkt in self.kkt:
            if kkt.kktSerial == serial:
                return kkt
        return None

    def get_opened_shifts(self) -> List[KktInfo]:
        """Получить кассы с открытой сменой"""
        return [kkt for kkt in self.kkt if kkt.shiftState == ShiftState.OPENED]