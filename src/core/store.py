# data_store.py
from dataclasses import dataclass, field
from typing import Optional, Dict, Any


@dataclass
class AppDataStore:
    """Простое хранилище данных приложения (синглтон через паттерн Module)"""

    # Данные пользователя из API

    gis_mt #данные об gis mt
    regime #данные об лм чз
    cash #данные о конкретной кассе
    esm #данные о конкретном экземпляре tspiot


    # Python модули - это синглтоны, просто импортируй этот объект
    # Создаём один экземпляр на весь модуль
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


# Создаём один экземпляр, который будем импортировать везде
store = AppDataStore()