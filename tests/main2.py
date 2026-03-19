import sys

from PySide6.QtCore import QObject, Signal, Slot, QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine


class SimpleController(QObject):
    """
    Простой контроллер с выбором Да/Нет
    """

    # Сигнал, который будет отправлять выбранное значение в QML
    selectionChanged = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        # Доступные варианты
        self.options = ["Да", "Нет"]

        # Текущий выбор
        self.current_selection = None

        print("✅ Контроллер создан")
        print(f"   Доступные варианты: {self.options}")

    @Slot(result=list)
    def getOptions(self):
        """Возвращает список вариантов для выпадающего списка"""
        return self.options

    @Slot(str)
    def selectOption(self, option: str):
        """Выбирает вариант и отправляет сигнал"""
        print(f"👉 Выбрано: {option}")
        self.current_selection = option
        self.selectionChanged.emit(option)

    @Slot(result=str)
    def getCurrentSelection(self):
        """Возвращает текущий выбранный вариант"""
        return self.current_selection if self.current_selection else "Ничего не выбрано"


def main():
    """Запуск приложения"""
    app = QGuiApplication(sys.argv)

    # Создаем движок QML
    engine = QQmlApplicationEngine()

    # Создаем контроллер
    controller = SimpleController()

    # Добавляем контроллер в контекст QML
    context = engine.rootContext()
    context.setContextProperty("simpleController", controller)

    # ✅ ПРАВИЛЬНЫЙ СПОСОБ: загружаем QML из ресурсов
    # Используем схему qrc:/ вместо file://
    qml_url = QUrl("qrc:/RegistrationButton.qml")
    print(f"📁 Загрузка QML из ресурсов: {qml_url.toString()}")

    # Загружаем QML
    engine.load(qml_url)

    # Проверка ошибок
    if not engine.rootObjects():
        print("❌ Ошибка: Не удалось загрузить QML файл")
        # Полезно для отладки - проверить, что ресурсы действительно загружены
        print("   Проверьте, что resources_rc.py создан и импортирован")
        sys.exit(-1)

    print("✅ Приложение запущено")
    sys.exit(app.exec())


if __name__ == "__main__":
    main()