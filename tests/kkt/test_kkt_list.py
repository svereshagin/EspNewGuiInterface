import sys
import os
from typing import List
from PySide6.QtCore import QObject, Slot, Property, Signal, QTimer, QUrl
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QMainWindow
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuickWidgets import QQuickWidget
from PySide6.QtGui import QFontDatabase, QIcon

# Импорты для тестовых данных
from domain.kkt.entity import CashInfo
from src.domain.common.regime_local_module import KktInfo, ShiftState


class KKTCommand:
    """Класс для тестирования - возвращает тестовые данные"""

    def __init__(self):
        self._cached_result = None
        print("🔧 KKTCommand инициализирован в тестовом режиме")

    def get_kkt_list(self) -> List[str]:
        """
        Возвращает тестовый список серийных номеров касс
        """
        print("🔍 get_kkt_list() вызван - используем ТЕСТОВЫЕ данные")

        # Создаем тестовые данные
        cash_info = CashInfo(
            kkt=[
                KktInfo(
                    kktSerial='00106327428745',
                    fnSerial='9999078902018941',
                    kktInn='9717169631',
                    kktRnm='0000000001040014',
                    modelName='АТОЛ FPrint-22ПТК',
                    dkktVersion='10.10.8.23',
                    developer='АТОЛ',
                    manufacturer='АТОЛ',
                    shiftState=ShiftState.CLOSED
                ),
                KktInfo(
                    kktSerial='00106327428746',
                    fnSerial='9999078902018942',
                    kktInn='7712345678',
                    kktRnm='0000000001040015',
                    modelName='АТОЛ FPrint-55ПТК',
                    dkktVersion='10.12.5.11',
                    developer='АТОЛ',
                    manufacturer='АТОЛ',
                    shiftState=ShiftState.OPENED
                ),
                KktInfo(
                    kktSerial='00234567890123',
                    fnSerial='8888123456789012',
                    kktInn='7722334455',
                    kktRnm='0000000001040016',
                    modelName='ШТРИХ-М-01Ф',
                    dkktVersion='5.2.3.1',
                    developer='ШТРИХ-М',
                    manufacturer='ШТРИХ-М',
                    shiftState=ShiftState.CLOSED
                )
            ]
        )

        cash_info = CashInfo(kkt=[])

        # Извлекаем серийные номера
        kkt_serials = []
        print(f"📦 Получены тестовые данные: {len(cash_info.kkt)} касс")

        for i, kkt in enumerate(cash_info.kkt, 1):
            kkt_serials.append(kkt.kktSerial)
            print(f"  {i}. Серийный номер: {kkt.kktSerial} - {kkt.modelName}")

        print(f"📊 Итоговый список серийных номеров: {kkt_serials}")
        return kkt_serials


class KKTController(QObject):
    """
    Контроллер для управления кассами
    """

    # Сигналы для обновления UI
    kktListChanged = Signal()
    selectedKktChanged = Signal()
    loadingChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        print("✅ KKTController инициализирован")
        self._kkt_list = []
        self._selected_kkt = ""
        self._is_loading = False
        self._kkt_command = KKTCommand()

        # Загружаем данные через 500 мс
        QTimer.singleShot(500, self.refresh_kkt_list)

    @Property(list, notify=kktListChanged)
    def kktList(self):
        """Возвращает список серийных номеров касс"""
        print(f"📋 kktList запрошен из QML, возвращает {len(self._kkt_list)} элементов: {self._kkt_list}")
        return self._kkt_list

    @Property(str, notify=selectedKktChanged)
    def selectedKkt(self):
        """Возвращает выбранный серийный номер"""
        return self._selected_kkt

    @Property(bool, notify=loadingChanged)
    def isLoading(self):
        """Флаг загрузки"""
        return self._is_loading

    @Slot()
    def refresh_kkt_list(self):
        """Обновляет список касс"""
        print("🔄 refresh_kkt_list вызван")

        self._is_loading = True
        self.loadingChanged.emit()

        try:
            # Получаем список серийных номеров
            new_kkt_list = self._kkt_command.get_kkt_list()

            # Обновляем список
            self._kkt_list = new_kkt_list

            print(f"✅ Список обновлен: {len(new_kkt_list)} элементов")
            print(f"📋 Новый список: {new_kkt_list}")

            # Отправляем сигнал об изменении
            self.kktListChanged.emit()

        except Exception as e:
            print(f"❌ Ошибка: {e}")
            self._kkt_list = []
            self.kktListChanged.emit()

        finally:
            self._is_loading = False
            self.loadingChanged.emit()

    @Slot(str)
    def select_kkt(self, kkt_serial: str):
        """Выбирает кассу по серийному номеру"""
        print(f"🎯 select_kkt({kkt_serial})")
        if self._selected_kkt != kkt_serial:
            self._selected_kkt = kkt_serial
            self.selectedKktChanged.emit()
            print(f"✅ Выбран серийный номер: {kkt_serial}")

    @Slot()
    def clear_selection(self):
        """Сбрасывает выбор"""
        print("🧹 clear_selection()")
        self._selected_kkt = ""
        self.selectedKktChanged.emit()

    @Slot(str, result=str)
    def get_kkt_status(self, kkt_serial: str) -> str:
        """Возвращает статус кассы (заглушка)"""
        if kkt_serial:
            # В реальном коде здесь можно получить статус по серийному номеру
            return "🟢 Активна"
        return "⚪ Не выбрана"


class TSPIoTQmlLoader(QMainWindow):
    def __init__(self,
                 window_size: tuple,
                 app_icon_path: str,
                 header_name: str,
                 fonts_path: str,
                 qml_file: str):
        super().__init__()

        # Создаем контроллер
        self._kkt_controller = KKTController()

        # Сохраняем параметры
        self.app_icon_path = app_icon_path
        self.header_name = header_name
        self.window_size = window_size
        self.qml_base_file = qml_file

        # Загружаем шрифты
        self.__load_fonts(fonts_path)

        # Устанавливаем параметры окна
        self.setWindowTitle(header_name)
        self.setFixedSize(window_size[0], window_size[1])
        self.__set_app_icon()

        # Создаем центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        # Создаем QQuickWidget
        self.quick_widget = QQuickWidget()

        # Регистрируем контроллер в контексте QML
        engine = self.quick_widget.engine()
        engine.rootContext().setContextProperty("kktController", self._kkt_controller)
        print("✅ Контроллер зарегистрирован в QML контексте как 'kktController'")

        # Загружаем QML
        qml_url = QUrl.fromLocalFile(qml_file)
        print(f"📁 Загрузка QML из: {qml_url.toString()}")

        self.quick_widget.setSource(qml_url)

        # Проверка ошибок
        if self.quick_widget.status() == QQuickWidget.Status.Error:
            print("❌ Ошибка загрузки QML:")
            for error in self.quick_widget.errors():
                print(f"   {error.toString()}")
        else:
            print("✅ QML успешно загружен")

        layout.addWidget(self.quick_widget)

    def __set_app_icon(self):
        if os.path.exists(self.app_icon_path):
            self.setWindowIcon(QIcon(self.app_icon_path))
            print(f"✅ Иконка загружена: {self.app_icon_path}")
        else:
            print(f"❌ Иконка не найдена: {self.app_icon_path}")

    def __load_fonts(self, fonts_dir):
        if not os.path.exists(fonts_dir):
            print(f"❌ Папка со шрифтами не найдена: {fonts_dir}")
            return

        print(f"📁 Загружаем шрифты из: {fonts_dir}")
        for font_file in os.listdir(fonts_dir):
            if font_file.endswith(('.ttf', '.otf', '.ttc')):
                font_path = os.path.join(fonts_dir, font_file)
                font_id = QFontDatabase.addApplicationFont(font_path)
                if font_id != -1:
                    font_families = QFontDatabase.applicationFontFamilies(font_id)
                    print(f"  ✅ Загружен: {font_file} -> {font_families}")


def main():
    # Параметры
    SRC_DIR = os.path.dirname(os.path.abspath(__file__))
    __WINDOW_SIZE = (400, 300)
    __APP_HEADER_TITLE = "ТС ПИоТ - Тест касс"
    __APP_ICON_PATH = os.path.join(SRC_DIR, "ui", "assets", "image_89.png")
    __FONTS_PATH = os.path.join(SRC_DIR, "ui", "fonts")
    __QML_PATH = os.path.join(SRC_DIR, "ui", "simple.qml")

    app = QApplication(sys.argv)

    # Создаем и показываем окно
    loader = TSPIoTQmlLoader(
        window_size=__WINDOW_SIZE,
        app_icon_path=__APP_ICON_PATH,
        header_name=__APP_HEADER_TITLE,
        fonts_path=__FONTS_PATH,
        qml_file=__QML_PATH
    )

    loader.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()