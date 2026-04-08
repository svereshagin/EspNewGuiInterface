import os
import sys
from functools import lru_cache


@lru_cache(maxsize=None)
def resource_path(relative_path):
    # Всегда ищем относительно папки с исполняемым файлом
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)  # папка с .exe
    else:
        current_file = os.path.abspath(__file__)  # .../old_src/infrastructure/utils/common.py
        # Поднимаемся на 3 уровня: utils/ -> infrastructure/ -> old_src/
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
    full_path = os.path.join(base_path, relative_path)
    return full_path



# ==================== ФУНКЦИЯ ПРОВЕРКИ РЕЖИМА КОМПИЛЯЦИИ ====================
def check_compile_mode():
    """Проверяет режим запуска (компиляция/разработка)"""
    if '--compiled' in sys.argv:
        sys.argv.remove('--compiled')
        return True
    if '--dev' in sys.argv:
        sys.argv.remove('--dev')
        return False
    return False
