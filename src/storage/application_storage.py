# storage/app_storage.py
from typing import Optional, Dict, List
from PySide6.QtCore import QObject, Signal
from src.dto.kkt import CashInfo, KktInfo
from src.services.kkt_service import KKTService
from src.storage.async_executor import AsyncExecutor
from src.storage.cache_manager import CacheManager
from src.storage.mappers.kkt_mapper import KktMapper


class AppStorage(QObject):
    """Хранилище состояния - только бизнес-логика"""

    kktListChanged = Signal()
    currentSerialChanged = Signal()
    loadingChanged = Signal(bool)  # Пробрасываем от AsyncExecutor
    errorChanged = Signal(str)  # Пробрасываем от AsyncExecutor

    def __init__(self, kkt_service: KKTService, cache_ttl_seconds: int = 300, parent=None, is_test=True):
        super().__init__(parent)
        self._service = kkt_service
        self.is_test = is_test

        # Менеджер ассинхронных запросов
        self._executor = AsyncExecutor(max_threads=3, parent=self)

        # Менеджер кэша
        self._cache = CacheManager[CashInfo](ttl_seconds=cache_ttl_seconds)

        # Пробрасываем сигналы
        self._executor.loadingChanged.connect(self.loadingChanged)
        self._executor.errorChanged.connect(self.errorChanged)

        # Данные
        self._kkt_list: List[dict] = []
        self._kkt_info_cache: Dict[str, dict] = {}
        self._current_serial: str = ""
        self._current_inn: str = ""


    # ─── Public Methods ─────────────────────────────────────────
    def load_kkt(self, reset: bool = False):
        """Асинхронно загружает список касс"""
        if not reset and self._cache.is_valid() and self._kkt_list:
            return

        def on_success(result: CashInfo):
            self._update_cache(result)
            self._cache.set(result)

            if not self._current_serial and self._kkt_list:
                self._current_serial = self._kkt_list[0].get('kktSerial', '')
                self.currentSerialChanged.emit()

            self.kktListChanged.emit()

        def on_error(error_msg: str):
            # Логирование ошибки
            print(f"Error loading KKT: {error_msg}")

        self._executor.execute(
            func=self._service.get_kkt_list,
            on_success=on_success,
            on_error=on_error,
            is_test=self.is_test,
            reset=reset
        )

    def reload_kkt(self):
        """Принудительная перезагрузка"""
        self.load_kkt(reset=True)


    def get_kkt_info(self, serial: str) -> dict:
        """Возвращает информацию о кассе из кэша"""
        return self._kkt_info_cache.get(serial, {})

    def set_current_cash(self, serial: str):
        """Устанавливает текущую кассу"""
        if self._current_serial != serial and serial in self._kkt_info_cache:
            self._current_serial = serial
            self.currentSerialChanged.emit()

    def set_current_inn(self, inn: str):
        self._current_inn = inn

    # ─── Properties ─────────────────────────────────────────────

    @property
    def kktList(self) -> List[dict]:
        return self._kkt_list

    @property
    def currentSerial(self) -> str:
        return self._current_serial

    @property
    def is_loading(self) -> bool:
        return self._executor.is_loading

    @property
    def error(self) -> str:
        return self._executor.error

    @property
    def get_unique_inn(self):
        if not self._kkt_list:
            return []
        return self._service.get_unique_cash_inn()

    # ─── Private Methods ────────────────────────────────────────
    def _update_cache(self, cash_info: CashInfo):
        """Обновляет внутренний кэш из DTO"""
        self._kkt_list.clear()
        self._kkt_info_cache.clear()

        for kkt in cash_info.kkt:
            kkt_dict = self._kkt_to_dict(kkt)
            self._kkt_list.append(kkt_dict)
            self._kkt_info_cache[kkt.kktSerial] = kkt_dict

    def _kkt_to_dict(self, kkt: KktInfo) -> dict:
        return KktMapper.to_dict(kkt)

