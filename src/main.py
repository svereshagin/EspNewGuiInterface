# main.py
import sys
import os
from pathlib import Path

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QUrl


sys.path.insert(0, str(Path(__file__).parent))

from src.services.kkt_service import KKTService
from src.services.tspiot import TSPIoTService
from src.storage.application_storage import AppStorage


def get_resource_path() -> str:
    """
    Onefile-совместимый путь к ресурсам.
    В dev-режиме — рядом с main.py.
    В PyInstaller onefile — из sys._MEIPASS.
    """
    if hasattr(sys, "_MEIPASS"):
        base = sys._MEIPASS
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, "ui/main.qml")


def main():
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()


    kkt_service = KKTService()
    tspiot_service = TSPIoTService()

    # Создаём хранилище
    app_storage = AppStorage(
        kkt_service=kkt_service,
        tspiot_service=tspiot_service,
        cache_ttl_seconds=300,
        is_test=False  # Режим тестирования отключён
    )

    # Регистрируем в QML
    engine.rootContext().setContextProperty("AppStorage", app_storage)

    # Путь к QML файлу
    qml_file = get_resource_path()
    engine.load(qml_file)

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()