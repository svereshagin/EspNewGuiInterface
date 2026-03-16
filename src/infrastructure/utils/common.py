import os
import sys


def get_base_path():
    """Возвращает базовый путь для ресурсов в зависимости от режима запуска"""
    if getattr(sys, 'frozen', False):
        # Запущено как собранное приложение
        return os.path.dirname(sys.executable)
    else:
        # Запущено как скрипт
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def resolve_path(relative_path):
    """
    Преобразует относительный путь в абсолютный, учитывая режим запуска.
    Сохраняет оригинальный относительный путь для констант.
    """
    base_path = get_base_path()

    # Убираем ../ из начала пути если они есть
    if relative_path.startswith('../'):
        # Считаем количество уровней подъема
        parts = relative_path.split('/')
        up_levels = sum(1 for p in parts if p == '..')

        # Поднимаемся на нужное количество уровней от base_path
        current = base_path
        for _ in range(up_levels):
            current = os.path.dirname(current)

        # Добавляем оставшуюся часть пути (без ../)
        remaining = '/'.join([p for p in parts if p != '..'])
        return os.path.join(current, remaining)
    else:
        # Если путь не начинается с .., просто присоединяем к base_path
        return os.path.join(base_path, relative_path)