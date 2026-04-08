# dto/kkt_dto.py
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Dict, Any


class ShiftState(str, Enum):
    """Состояние смены"""
    CLOSED = "Закрыта"
    OPENED = "Открыта"
    EXPIRED = "Истекла"


@dataclass
class KktInfo:
    """Информация о конкретной кассе (чистый DTO)"""
    kktSerial: str
    fnSerial: str
    kktInn: str
    kktRnm: str
    modelName: str
    dkktVersion: str
    developer: str
    manufacturer: str
    shiftState: ShiftState

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'KktInfo':
        """Создание из словаря (только парсинг)"""
        return cls(
            kktSerial=data.get('kktSerial', '').strip(),
            fnSerial=data.get('fnSerial', '').strip(),
            kktInn=data.get('kktInn', '').strip(),
            kktRnm=data.get('kktRnm', '').strip(),
            modelName=data.get('modelName', '').strip(),
            dkktVersion=data.get('dkktVersion', '').strip(),
            developer=data.get('developer', '').strip(),
            manufacturer=data.get('manufacturer', '').strip(),
            shiftState=ShiftState(data.get('shiftState', 'Закрыта').strip())
        )

    def to_dict(self) -> Dict[str, Any]:
        """Преобразование в словарь для сериализации"""
        return {
            'kktSerial': self.kktSerial,
            'fnSerial': self.fnSerial,
            'kktInn': self.kktInn,
            'kktRnm': self.kktRnm,
            'modelName': self.modelName,
            'dkktVersion': self.dkktVersion,
            'developer': self.developer,
            'manufacturer': self.manufacturer,
            'shiftState': self.shiftState.value
        }


@dataclass
class CashInfo:
    """Информация о подключенных кассах (чистый DTO)"""
    kkt: List[KktInfo] = field(default_factory=list)

    @classmethod
    def from_api_response(cls, response_data: Dict[str, Any]) -> 'CashInfo':
        """Создание из ответа API"""
        kkt_list = []
        if 'kkt' in response_data and isinstance(response_data['kkt'], list):
            for kkt_item in response_data['kkt']:
                try:
                    kkt_list.append(KktInfo.from_dict(kkt_item))
                except (KeyError, ValueError) as e:
                    print(f"Ошибка парсинга кассы: {e}")
                    continue
        return cls(kkt=kkt_list)

    def __len__(self) -> int:
        return len(self.kkt)

    def __getitem__(self, index: int) -> KktInfo:
        return self.kkt[index]