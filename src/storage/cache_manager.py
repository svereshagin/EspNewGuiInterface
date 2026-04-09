# storage/cache_manager.py
from typing import Generic, TypeVar, Optional
from datetime import datetime, timedelta
from PySide6.QtCore import QMutex, QMutexLocker

T = TypeVar('T')


class CacheManager(Generic[T]):
    """Универсальный менеджер кэша с TTL"""

    def __init__(self, ttl_seconds: int = 300):
        self._cache: Optional[T] = None
        self._last_update: Optional[datetime] = None
        self._ttl = ttl_seconds
        self._mutex = QMutex()

    def get(self) -> Optional[T]:
        with QMutexLocker(self._mutex):
            if self._is_valid():
                return self._cache
            return None

    def set(self, data: T):
        with QMutexLocker(self._mutex):
            self._cache = data
            self._last_update = datetime.now()

    def clear(self):
        with QMutexLocker(self._mutex):
            self._cache = None
            self._last_update = None

    def is_valid(self) -> bool:
        with QMutexLocker(self._mutex):
            return self._is_valid()

    def _is_valid(self) -> bool:
        if self._cache is None or self._last_update is None:
            return False
        return datetime.now() - self._last_update < timedelta(seconds=self._ttl)