import sys
import os
from PySide6.QtCore import QObject, Slot, Property, Signal
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine


class ItemModel(QObject):
    """Модель данных для элементов списка"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._items = ["Яблоко", "Банан", "Апельсин", "Груша", "Виноград"]
        self._selected_item = ""

    # Сигналы для обновления UI
    itemsChanged = Signal()
    selectedItemChanged = Signal()

    # Получить список элементов
    @Property(list, notify=itemsChanged)
    def items(self):
        return self._items

    # Получить выбранный элемент
    @Property(str, notify=selectedItemChanged)
    def selectedItem(self):
        return self._selected_item

    # Установить выбранный элемент
    @Slot(str)
    def selectItem(self, item):
        if self._selected_item != item:
            self._selected_item = item
            self.selectedItemChanged.emit()
            print(f"Выбран элемент: {item}")


class Backend(QObject):
    """Основной backend класс для связи с QML"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._item_model = ItemModel()

    @Property(QObject, constant=True)
    def itemModel(self):
        return self._item_model


if __name__ == "__main__":
    app = QGuiApplication(sys.argv)

    # Создаем движок QML
    engine = QQmlApplicationEngine()

    # Создаем backend и регистрируем его в QML контексте
    backend = Backend()
    engine.rootContext().setContextProperty("backend", backend)

    # Загружаем QML файл
    qml_file = os.path.join(os.path.dirname(__file__), "main.qml")
    engine.load(qml_file)

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())