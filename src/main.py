import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtCore import QUrl
from PySide6.QtQuickWidgets import QQuickWidget
from PySide6.QtGui import QFontDatabase, QIcon

from src.infrastructure.utils.qml_loader import TSPIoTQmlLoader

__WINDOW_SIZE = (829, 612)
__APP_ICON_PATH = "../ui/assets/image_89.png"
__APP_HEADER_TITLE = "ТС ПИоТ"
__FONTS_PATH = "../ui/fonts"


#
#         # Создаем центральный виджет
#         central_widget = QWidget()
#         self.setCentralWidget(central_widget)
#
#         # Создаем layout
#         layout = QVBoxLayout(central_widget)
#
#         # Создаем виджет для QML
#         self.quick_widget = QQuickWidget()
#
#         # Указываем путь к вашему QML файлу
#         qml_path = os.path.abspath("../ui/Gadget.ui.qml")
#         self.quick_widget.setSource(QUrl.fromLocalFile(qml_path))
#
#         # Добавляем в layout
#         layout.addWidget(self.quick_widget)
#
#         # Если что-то пошло не так, покажем ошибку
#         if self.quick_widget.status() != QQuickWidget.Status.Ready:
#             print("Ошибка загрузки QML:", self.quick_widget.errors())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    tspiot = TSPIoTQmlLoader(window_size=__WINDOW_SIZE, app_icon_path=__APP_ICON_PATH, header_name=__APP_HEADER_TITLE,fonts_path=__FONTS_PATH)
    # window = MainWindow()
    tspiot.show()
    sys.exit(app.exec())