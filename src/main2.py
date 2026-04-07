import sys
from PySide6.QtCore import QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

# Импортируем контроллер
from controllers.controlmodule import ControlModuleViewModel

# Импортируем скомпилированные ресурсы
import resources_rc

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    # Создаем контроллер
    mainController = ControlModuleViewModel()

    # Регистрируем контроллер в QML контексте
    engine.rootContext().setContextProperty("mainController", mainController)

    # Загружаем QML из ресурсов
    engine.load(QUrl("qrc:/ui/MainView.qml"))

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())