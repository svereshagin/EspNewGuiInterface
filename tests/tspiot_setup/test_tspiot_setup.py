import sys
import os

from typing import List, Optional
from PySide6.QtCore import QObject, Slot, Property, Signal, QTimer, QUrl, QThread
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QMainWindow
from PySide6.QtQuickWidgets import QQuickWidget
from PySide6.QtGui import QFontDatabase, QIcon

# Импорты для работы с сетью
from src.network.tspiot import TspiotSetup, RequestCreateInstanceTSPIOT_DTO, TspiotResult


class RegistrationWorker(QObject):
    """Рабочий класс для выполнения регистрации в отдельном потоке"""

    finished = Signal(object)  # TspiotResult
    error = Signal(str)

    def __init__(self):
        super().__init__()
        print("🔧 RegistrationWorker инициализирован")
        self._tspiot = TspiotSetup()

    @Slot(str)
    def register(self, kkt_serial: str):
        """Выполняет регистрацию в потоке"""
        try:
            print(f"🔄 Регистрация для ККТ: {kkt_serial}")
            dto = RequestCreateInstanceTSPIOT_DTO(kkt_serial=kkt_serial)
            result = self._tspiot.create_esm_service(dto)
            print(f"✅ Регистрация завершена: {result}")
            self.finished.emit(result)
        except Exception as e:
            print(f"❌ Ошибка регистрации: {e}")
            self.error.emit(str(e))


class RegistrationController(QObject):
    """
    Контроллер для регистрации ТС ПИоТ
    """

    # Сигналы для UI
    isRegisteredChanged = Signal()
    isLoadingChanged = Signal()
    errorChanged = Signal()
    resultChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        print("✅ RegistrationController инициализирован")

        self._is_registered: bool = False
        self._is_loading: bool = False
        self._error: Optional[str] = None
        self._last_result: Optional[TspiotResult] = None

        # Для работы с потоками
        self._thread: Optional[QThread] = None
        self._worker: Optional[RegistrationWorker] = None

    @Property(bool, notify=isRegisteredChanged)
    def isRegistered(self):
        return self._is_registered

    @Property(bool, notify=isLoadingChanged)
    def isLoading(self):
        return self._is_loading

    @Property(str, notify=errorChanged)
    def error(self):
        return self._error or ""

    @Property(object, notify=resultChanged)
    def lastResult(self):
        return self._last_result

    @Slot(str)
    def register(self, kkt_serial: str):
        """Запускает регистрацию"""
        if self._is_loading:
            print("⚠️ Регистрация уже выполняется")
            return

        print(f"🚀 Запуск регистрации для ККТ: {kkt_serial}")

        self._is_loading = True
        self._error = None
        self.isLoadingChanged.emit()
        self.errorChanged.emit()

        # Останавливаем предыдущий поток
        self._stop_thread()

        # Создаем новый поток
        self._thread = QThread()
        self._worker = RegistrationWorker()
        self._worker.moveToThread(self._thread)

        # Подключаем сигналы
        self._thread.started.connect(lambda: self._worker.register(kkt_serial))
        self._worker.finished.connect(self._on_registration_finished)
        self._worker.error.connect(self._on_registration_error)
        self._worker.finished.connect(self._cleanup_thread)
        self._worker.error.connect(self._cleanup_thread)

        # Запускаем поток
        self._thread.start()

    def _on_registration_finished(self, result: TspiotResult):
        """Обработка успешной регистрации"""
        print(f"✅ Регистрация завершена: success={result.success}")

        self._last_result = result
        self.resultChanged.emit()

        if result.success:
            self._is_registered = True
            self._error = None
            print(f"✅ Успешно зарегистрировано. ID: {result.tspiot_id}")
        else:
            self._is_registered = False
            self._error = result.error_message or "Неизвестная ошибка"

        self.isRegisteredChanged.emit()
        self.errorChanged.emit()

        self._is_loading = False
        self.isLoadingChanged.emit()

    def _on_registration_error(self, error_msg: str):
        """Обработка ошибки"""
        print(f"❌ Ошибка: {error_msg}")

        self._is_registered = False
        self._error = error_msg
        self._last_result = None

        self.isRegisteredChanged.emit()
        self.errorChanged.emit()
        self.resultChanged.emit()

        self._is_loading = False
        self.isLoadingChanged.emit()

    @Slot()
    def reset(self):
        """Сбрасывает состояние"""
        print("🔄 Сброс состояния")

        self._is_registered = False
        self._is_loading = False
        self._error = None
        self._last_result = None

        self._stop_thread()

        self.isRegisteredChanged.emit()
        self.isLoadingChanged.emit()
        self.errorChanged.emit()
        self.resultChanged.emit()

    def _stop_thread(self):
        if self._thread and self._thread.isRunning():
            self._thread.quit()
            self._thread.wait(1000)

    def _cleanup_thread(self):
        if self._thread:
            self._thread.quit()
            self._thread.wait(1000)
            if self._worker:
                self._worker.deleteLater()
                self._worker = None
            self._thread.deleteLater()
            self._thread = None

    def __del__(self):
        self._stop_thread()


class TSPIoTQmlLoader(QMainWindow):
    def __init__(self,
                 window_size: tuple,
                 app_icon_path: str,
                 header_name: str,
                 fonts_path: str,
                 qml_file: str):
        super().__init__()

        # Создаем контроллер
        self._registration_controller = RegistrationController()

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
        self.quick_widget.setResizeMode(QQuickWidget.SizeRootObjectToView)

        # Регистрируем контроллер в контексте QML
        engine = self.quick_widget.engine()
        engine.rootContext().setContextProperty("registrationController", self._registration_controller)
        print("✅ Контроллер зарегистрирован в QML контексте как 'registrationController'")

        # Загружаем QML
        qml_url = QUrl.fromLocalFile(qml_file)
        print(f"📁 Загрузка QML из: {qml_url.toString()}")
        self.quick_widget.setSource(qml_url)

        # Проверка ошибок
        if self.quick_widget.status() == QQuickWidget.Error:
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

    def __load_fonts(self, fonts_dir):
        if not os.path.exists(fonts_dir):
            return
        for font_file in os.listdir(fonts_dir):
            if font_file.endswith(('.ttf', '.otf', '.ttc')):
                font_path = os.path.join(fonts_dir, font_file)
                QFontDatabase.addApplicationFont(font_path)


def main():
    # Параметры
    SRC_DIR = os.path.dirname(os.path.abspath(__file__))
    __WINDOW_SIZE = (400, 250)
    __APP_HEADER_TITLE = "ТС ПИоТ - Регистрация"
    __APP_ICON_PATH = os.path.join(SRC_DIR, "ui", "assets", "image_89.png")
    __FONTS_PATH = os.path.join(SRC_DIR, "ui", "fonts")
    __QML_PATH = os.path.join(SRC_DIR, "ui", "RegistrationButton.qml")

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