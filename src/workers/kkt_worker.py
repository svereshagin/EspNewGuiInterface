# workers/kkt_worker.py
from typing import Callable
from PySide6.QtCore import QObject, Signal, QRunnable


class KKTWorkerSignals(QObject):
    """Сигналы для коммуникации между потоком и главным потоком"""
    finished = Signal(object)  # Результат
    error = Signal(str)  # Сообщение об ошибке
    progress = Signal(str)  # Прогресс/статус


class KKTWorker(QRunnable):
    """
    Worker - ТОЛЬКО выполняет переданную функцию в отдельном потоке.
    Не содержит бизнес-логики!
    """

    def __init__(self, func: Callable, *args, **kwargs):
        """
        Args:
            func: Функция для выполнения (метод сервиса)
            *args, **kwargs: Аргументы для функции
        """
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.signals = KKTWorkerSignals()
        self._is_cancelled = False

    def run(self):
        """Выполняется в отдельном потоке"""
        try:
            # Эмитим прогресс (опционально)
            self.signals.progress.emit(f"Выполняю {self.func.__name__}...")

            # Вызываем функцию с переданными аргументами
            result = self.func(*self.args, **self.kwargs)

            # Отправляем результат в главный поток
            if not self._is_cancelled:
                self.signals.finished.emit(result)

        except Exception as e:
            if not self._is_cancelled:
                self.signals.error.emit(str(e))

    def cancel(self):
        """Отмена операции"""
        self._is_cancelled = True