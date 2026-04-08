# storage/app_storage.py
from typing import Optional, Dict, Any, List, Callable
from datetime import datetime, timedelta
from PySide6.QtCore import QObject, Signal, QThreadPool, QMutex, QMutexLocker
from src.dto.kkt import CashInfo, KktInfo
from src.services.kkt_service import KKTService
from src.workers.kkt_worker import KKTWorker





class AppStorage(QObject):
    """
    Хранилище состояния с асинхронной загрузкой через воркеров
    """

    kktListChanged = Signal()
    currentSerialChanged = Signal()
    loadingChanged = Signal()
    errorChanged = Signal()

    def __init__(self, kkt_service: KKTService, cache_ttl_seconds: int = 300, parent=None, is_test=True):
        super().__init__(parent)
        self._service = kkt_service
        self._cache_ttl = cache_ttl_seconds

        # Thread pool для выполнения воркеров
        self._threadpool = QThreadPool()
        self._threadpool.setMaxThreadCount(3)

        # Тест?
        self.is_test = is_test

        # Данные
        self._kkt_list: list = []
        self._kkt_info_cache: Dict[str, dict] = {}
        self._current_inn: str = ""
        self._current_serial: str = ""
        self._is_loading: bool = False
        self._error: str = ""
        self._last_update: Optional[datetime] = None

        # Активные воркеры
        self._active_workers = 0
        self._mutex = QMutex()


    # ─── Public Methods ─────────────────────────────────────────
    def load_kkt(self, reset: bool = False):
        """Асинхронно загружает список касс"""
        if not reset and self._is_cache_valid() and self._kkt_list:
            return

        def on_success(result: Optional[CashInfo]):
            if result is None:
                self._set_error("Не удалось загрузить список касс")
            else:
                with QMutexLocker(self._mutex):
                    self._update_cache(result)
                    self._last_update = datetime.now()

                    # Добавляем эмит сигналов
                    if not self._current_serial and self._kkt_list:
                        self._current_serial = self._kkt_list[0].get('kktSerial', '')
                        self.currentSerialChanged.emit()

                    self.kktListChanged.emit()

        self._execute_async(
            func=self._service.get_kkt_list,
            on_finished=lambda result: self._on_worker_success(result, on_success),
            on_error=self._on_worker_error,
            is_test=self.is_test,
            reset=reset
        )


    def reload_kkt(self):
        self.load_kkt(reset=True)



    def get_shift_states_async(self):
        """Асинхронно получить кассы с открытыми сменами"""
        ...


    def get_kkt_info(self, serial: str) -> dict:
        """Возвращает информацию о кассе из кэша"""
        with QMutexLocker(self._mutex):
            return self._kkt_info_cache.get(serial, {})


    def set_current_cash(self, serial: str):
        """Устанавливает текущую кассу"""
        if self._current_serial != serial and serial in self._kkt_info_cache:
            self._current_serial = serial
            self.currentSerialChanged.emit()

    def set_current_inn(self, inn: str):
        self._current_inn = inn

    @property
    def get_unique_inn(self):
        if not self._kkt_list:
            ...
        return self._service.get_unique_cash_inn()



    @property
    def kktList(self) -> list:
        return self._kkt_list

    @property
    def currentSerial(self) -> str:
        """
        Выбираем текущую кассу по её серийному номеру
        """
        return self._current_serial

    @property
    def is_loading(self) -> bool:
        return self._is_loading

    @property
    def error(self) -> str:
        return self._error

    # ─── Private Methods ────────────────────────────────────────

    def _is_cache_valid(self) -> bool:
        if self._last_update is None:
            return False
        return datetime.now() - self._last_update < timedelta(seconds=self._cache_ttl)


    def _set_loading(self, loading: bool):
        self._is_loading = loading
        self.loadingChanged.emit()


    def _set_error(self, error: str):
        self._error = error
        self.errorChanged.emit()


    def _update_cache(self, cash_info: CashInfo):
        """Обновляет кэш из DTO"""
        self._kkt_list.clear()
        self._kkt_info_cache.clear()

        for kkt in cash_info.kkt:
            kkt_dict = self._kkt_to_dict(kkt)
            self._kkt_list.append(kkt_dict)
            self._kkt_info_cache[kkt.kktSerial] = kkt_dict

    def _kkt_to_dict(self, kkt: KktInfo) -> dict:
        return {
            'kktSerial': kkt.kktSerial,
            'fnSerial': kkt.fnSerial,
            'kktInn': kkt.kktInn,
            'kktRnm': kkt.kktRnm,
            'modelName': kkt.modelName,
            'dkktVersion': kkt.dkktVersion,
            'developer': kkt.developer,
            'manufacturer': kkt.manufacturer,
            'shiftState': kkt.shiftState.value,
            'displayName': f"{kkt.kktRnm} ({kkt.kktSerial})",
            'isShiftOpen': kkt.shiftState.value
        }

    def _execute_async(
            self,
            func: Callable,
            on_finished: Callable,
            on_error: Optional[Callable] = None,
            *args,
            **kwargs
    ):
        """
        Универсальный метод для асинхронного выполнения задач
        """
        if self._is_loading:
            # Не начинаем новую загрузку, если уже идёт
            return

        self._set_loading(True)
        self._set_error("")

        # Создаём воркер
        worker = KKTWorker(func, *args, **kwargs)

        worker.signals.finished.connect(on_finished)
        worker.signals.error.connect(on_error or self._on_worker_error)

        if not hasattr(self, '_active_workers_list'):
            self._active_workers_list = []
        self._active_workers_list.append(worker)

        self._active_workers += 1
        self._threadpool.start(worker)

    def _on_default_error(self, error_msg: str):
        """Обработчик ошибок по умолчанию"""
        self._on_worker_error(error_msg)

    def _on_worker_success(self, result, on_success: Callable):
        """Обёртка для успешного завершения"""
        self._active_workers -= 1

        if result is not None:
            on_success(result)
        else:
            self._set_error("Получен пустой результат")

        if self._active_workers == 0:
            self._set_loading(False)

    def _on_worker_error(self, error_msg: str):
        """Общая обработка ошибок"""
        self._active_workers -= 1
        self._set_error(error_msg)

        if self._active_workers == 0:
            self._set_loading(False)