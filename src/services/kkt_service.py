from typing import List, Optional
from src.dto.kkt import CashInfo, KktInfo, ShiftState


class KktService:
    """Сервис для работы с ККТ"""

    def __init__(self):
        """
        Без DI - просто передаём DTO в конструктор
        """
        self.cash_info: Optional[CashInfo] = None


    def get_all_cash_with_the_same_url(self, inn: str) -> List[KktInfo]:
        """
            Возвращает все kkt принадлежащие по признаку идемпотентности INN
            arg: inn - str
        """
        return [kkt for kkt in self.cash_info.kkt if kkt.kktInn == inn]

    def get_serial_numbers(self) -> List[str]:
        """Получить список серийных номеров всех касс"""
        return [kkt.kktSerial for kkt in self.cash_info.kkt]

    def is_shift_opened(self, kkt: KktInfo) -> bool:
        return True if kkt.shiftState == ShiftState.OPENED else False

    # def get_cash_states(self, cash_info: CashInfo ):
    #
    #     return {
    #         ""
    #     }