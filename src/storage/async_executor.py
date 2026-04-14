# storage/async_executor.py
from typing import Callable, Optional, List
from PySide6.QtCore import QObject, Signal, QThreadPool, QMutex
from src.workers.kkt_worker import KKTWorker


class AsyncExecutor(QObject):
    """Управляет асинхронным выполнением задач в потоках"""

    loadingChanged = Signal(bool)
    errorChanged = Signal(str)

    def __init__(self, max_threads: int = 3, parent=None):
        super().__init__(parent)
        self._threadpool = QThreadPool()
        self._threadpool.setMaxThreadCount(max_threads)
        self._active_workers = 0
        self._active_workers_list: List[KKTWorker] = []
        self._mutex = QMutex()
        self._is_loading = False
        self._error = ""

    @property
    def is_loading(self) -> bool:
        return self._is_loading

    @property
    def error(self) -> str:
        return self._error

    def execute(
            self,
            func: Callable,
            on_success: Optional[Callable] = None,
            on_error: Optional[Callable] = None,
            *args,
            **kwargs
    ):
        """Выполнить функцию асинхронно"""
        print("IS LOADING:", self._is_loading)
        # if self._is_loading:
        #     return False

        self._set_loading(True)
        self._set_error("")

        def on_finished(result):
            self._active_workers -= 1

            if result is not None and on_success:
                on_success(result)
            elif result is None and on_error:
                on_error("Получен пустой результат")

            if self._active_workers == 0:
                self._set_loading(False)

        def on_error_handler(error_msg: str):
            self._active_workers -= 1
            self._set_error(error_msg)
            if on_error:
                on_error(error_msg)
            if self._active_workers == 0:
                self._set_loading(False)

        worker = KKTWorker(func, *args, **kwargs)
        worker.signals.finished.connect(on_finished)
        worker.signals.error.connect(on_error_handler)

        self._active_workers_list.append(worker)
        self._active_workers += 1
        self._threadpool.start(worker)
        return True

    def _set_loading(self, loading: bool):
        self._is_loading = loading
        self.loadingChanged.emit(loading)

    def _set_error(self, error: str):
        self._error = error
        if error:
            self.errorChanged.emit(error)