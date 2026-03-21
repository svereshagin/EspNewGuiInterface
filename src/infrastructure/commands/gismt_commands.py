import os
import sys


def resource_path(relative_path):
    # Всегда ищем относительно папки с исполняемым файлом
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)  # папка с .exe
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)