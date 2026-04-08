import logging
from typing import List, Optional
from src.dto.kkt import CashInfo, KktInfo, ShiftState
from src.network.kkt import KKTNetwork

logger =  logging.getLogger(__name__)


class KKTService:
    """
    Сервис для работы с кассами.
    Содержит ВСЮ бизнес-логику.
    Worker будет вызывать методы этого класса.
    """

    def __init__(self):
        """
        Без DI - просто передаём DTO в конструктор
        """
        self.cash_info: Optional[CashInfo] = None
        self.dkkt_agent = KKTNetwork()
        self.unique_inns: list[str] = []


    def get_kkt_list(self, reset=False, is_test=False) -> Optional[CashInfo]:
        """
        Получить список всех касс

        reset: bool - сброс кэша (перезапись текущих данных)
        is_test: bool - чтобы перейти в режим тестирования без кассового ПО(UI)
        """
        if is_test:
            self.load_test_data()
        logger.debug("Запрос списка касс через сервис")
        if not self.cash_info or reset:
            self.cash_info = self.dkkt_agent.get_dkkt_list()
        return self.cash_info

    def get_unique_cash_inn(self):
        """
        После первого вызова делает "кэш" на уровне сервиса
        также возвращает уникальные INN
        """
        ununique_inns = []
        self.unique_inns = [inn for inn in self.cash_info.kkt if inn not in ununique_inns]
        return self.unique_inns



    def get_all_cash_within_unique_inn(self, inn: str) -> List[KktInfo]:
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


    def load_test_data(self, cash_quantity = 10):
        from src.tests.cash_test_data import TWO_CASH, ONE_CASH, ELEVEN_CASH, CASHES_WITH_SAME_INN, TEN_CASH
        cash_data_map = {
            1: ONE_CASH,
            2: TWO_CASH,
            10: TEN_CASH,
            12: ELEVEN_CASH,
            12_1: CASHES_WITH_SAME_INN
        }

        self.cash_info = CashInfo.from_api_response(cash_data_map.get(cash_quantity))