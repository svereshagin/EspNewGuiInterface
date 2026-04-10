# storage/cache_manager.py
from typing import Generic, TypeVar, Optional
from datetime import datetime, timedelta
from PySide6.QtCore import QMutex, QMutexLocker

T = TypeVar('T')

# storage/cache_manager.py
from typing import Generic, TypeVar, Optional, Dict
from datetime import datetime, timedelta
from PySide6.QtCore import QMutex, QMutexLocker

T = TypeVar('T')


class CacheManager(Generic[T]):
    """
    Универсальный менеджер кэша с TTL и поддержкой ключей
    """

    def __init__(self, ttl_seconds: int = 300):
        self._cache: Dict[str, T] = {}  # ключ -> данные
        self._timestamps: Dict[str, datetime] = {}  # ключ -> время обновления
        self._ttl = ttl_seconds
        self._mutex = QMutex()

    def get(self, key: str = "default") -> Optional[T]:
        """
        Получить данные по ключу

        Args:
            key: Ключ кэша (по умолчанию "default")

        Returns:
            Данные или None если нет в кэше
        """
        with QMutexLocker(self._mutex):
            if self._is_valid(key):
                return self._cache.get(key)
            return None

    def set(self, data: T, key: str = "default", ttl_seconds: Optional[int] = None):
        """
        Сохранить данные в кэш по ключу

        Args:
            data: Данные для сохранения
            key: Ключ кэша (по умолчанию "default")
            ttl_seconds: Индивидуальный TTL для этого ключа (опционально)
        """
        with QMutexLocker(self._mutex):
            self._cache[key] = data
            self._timestamps[key] = datetime.now()
            # Если нужен индивидуальный TTL, храним отдельно
            if ttl_seconds is not None:
                if not hasattr(self, '_custom_ttl'):
                    self._custom_ttl: Dict[str, int] = {}
                self._custom_ttl[key] = ttl_seconds

    def clear(self, key: Optional[str] = None):
        """
        Очистить кэш

        Args:
            key: Если указан - очистить только этот ключ, иначе весь кэш
        """
        with QMutexLocker(self._mutex):
            if key is None:
                self._cache.clear()
                self._timestamps.clear()
                if hasattr(self, '_custom_ttl'):
                    self._custom_ttl.clear()
            else:
                self._cache.pop(key, None)
                self._timestamps.pop(key, None)
                if hasattr(self, '_custom_ttl'):
                    self._custom_ttl.pop(key, None)

    def is_valid(self, key: str = "default") -> bool:
        """
        Проверить валидность кэша по ключу

        Args:
            key: Ключ для проверки
        """
        with QMutexLocker(self._mutex):
            return self._is_valid(key)

    def get_ttl(self, key: str = "default") -> int:
        """Получить TTL для ключа"""
        if hasattr(self, '_custom_ttl') and key in self._custom_ttl:
            return self._custom_ttl[key]
        return self._ttl

    def invalidate(self, key: Optional[str] = None):
        """Алиас для clear() - инвалидация кэша"""
        self.clear(key)

    def keys(self) -> list:
        """Получить все ключи в кэше"""
        with QMutexLocker(self._mutex):
            return list(self._cache.keys())

    def size(self) -> int:
        """Количество элементов в кэше"""
        with QMutexLocker(self._mutex):
            return len(self._cache)

    def _is_valid(self, key: str) -> bool:
        """Внутренняя проверка валидности (без блокировки)"""
        if key not in self._cache or key not in self._timestamps:
            return False

        ttl = self.get_ttl(key)
        return datetime.now() - self._timestamps[key] < timedelta(seconds=ttl)