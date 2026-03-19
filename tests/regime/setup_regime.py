import sys
import os
from typing import Optional
from datetime import datetime

from PySide6.QtCore import QObject, Slot, Property, Signal, QTimer, QUrl
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QMainWindow
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuickWidgets import QQuickWidget
from PySide6.QtGui import QFontDatabase, QIcon

from src.network.regime_local_module import (
    RegimeNetwork,
    RequestGetInfoRegime,
    RequestSetupRegime,
    ResponseGetInfoRegime,
    ResponseGetSettingsRegime
)


class RegimeController(QObject):
    """
    Контроллер для управления режимом ЛМ ЧЗ
    """

    # Сигналы для обновления UI
    regimeInfoChanged = Signal()
    settingsChanged = Signal()
    loadingChanged = Signal()
    errorChanged = Signal()

    def __init__(self, esm_instance_id: str, parent=None):
        super().__init__(parent)
        print(f"✅ RegimeController инициализирован для instance: {esm_instance_id}")

        self._esm_instance_id = esm_instance_id
        self._regime_info: Optional[ResponseGetInfoRegime] = None
        self._settings: Optional[ResponseGetSettingsRegime] = None
        self._is_loading = False
        self._error_message = ""

        self._network = RegimeNetwork()

        # Загружаем данные через 500 мс
        QTimer.singleShot(500, self.refresh_all)

    @Property(str, notify=regimeInfoChanged)
    def status(self) -> str:
        """Статус контроллера"""
        if self._regime_info and self._regime_info.lmStatus:
            status = self._regime_info.lmStatus.status
            operation_mode = self._regime_info.lmStatus.operationMode

            if status == "ready" and operation_mode == "active":
                return "🟢 Активен"
            elif status == "ready":
                return "🟡 Готов"
            else:
                return f"🔴 {status}"
        return "⚪ Неизвестно"

    @Property(str, notify=regimeInfoChanged)
    def version(self) -> str:
        """Версия контроллера"""
        if self._regime_info:
            return self._regime_info.controllerVersion
        return "—"

    @Property(str, notify=settingsChanged)
    def ip(self) -> str:
        """IP адрес"""
        if self._settings:
            return self._settings.address
        return "—"

    @Property(str, notify=regimeInfoChanged)
    def lastSync(self) -> str:
        """Последняя синхронизация"""
        if self._regime_info and self._regime_info.lmStatus:
            timestamp = self._regime_info.lmStatus.lastSync / 1000  # конвертируем из миллисекунд
            dt = datetime.fromtimestamp(timestamp)
            return dt.strftime("%d.%m.%Y %H:%M:%S")
        return "—"

    @Property(str, notify=regimeInfoChanged)
    def inn(self) -> str:
        """ИНН"""
        if self._regime_info and self._regime_info.lmStatus:
            return self._regime_info.lmStatus.inn
        return "—"

    @Property(str, notify=settingsChanged)
    def login(self) -> str:
        """Логин"""
        if self._settings:
            return self._settings.login
        return "—"

    @Property(bool, notify=loadingChanged)
    def isLoading(self) -> bool:
        """Флаг загрузки"""
        return self._is_loading

    @Property(str, notify=errorChanged)
    def errorMessage(self) -> str:
        """Сообщение об ошибке"""
        return self._error_message

    @Slot()
    def refresh_all(self):
        """Обновляет все данные"""
        print("🔄 refresh_all вызван")
        self._is_loading = True
        self.loadingChanged.emit()

        self.refresh_info()
        self.refresh_settings()

    @Slot()
    def refresh_info(self):
        """Обновляет информацию о режиме"""
        print("🔄 refresh_info вызван")

        try:
            info = self._network.get_regime_config_by_instance(
                RequestGetInfoRegime(esm_instance_id=self._esm_instance_id)
            )

            if info:
                self._regime_info = info
                self._error_message = ""
                print(f"✅ Информация получена: версия {info.controllerVersion}")
            else:
                self._error_message = "Не удалось получить информацию"

        except Exception as e:
            self._error_message = f"Ошибка: {e}"
            print(f"❌ Ошибка: {e}")

        self.regimeInfoChanged.emit()
        self.errorChanged.emit()
        self._finish_loading_if_done()

    @Slot()
    def refresh_settings(self):
        """Обновляет настройки"""
        print("🔄 refresh_settings вызван")

        try:
            settings = self._network.get_regime_settings_by_instance(
                RequestGetInfoRegime(esm_instance_id=self._esm_instance_id)
            )

            if settings:
                self._settings = settings
                print(f"✅ Настройки получены: {settings.address}:{settings.port}")
            else:
                # Если настроек нет, создаем пустые
                self._settings = ResponseGetSettingsRegime(
                    address="",
                    port=0,
                    login="",
                    password=""
                )

        except Exception as e:
            print(f"❌ Ошибка получения настроек: {e}")

        self.settingsChanged.emit()
        self._finish_loading_if_done()

    @Slot(str, int, str, str)
    def save_settings(self, address: str, port: int, login: str, password: str):
        """Сохраняет настройки"""
        print(f"💾 save_settings: {address}:{port}, {login}")

        self._is_loading = True
        self.loadingChanged.emit()

        try:
            request = RequestSetupRegime(
                esm_instance_id=self._esm_instance_id,
                address=address,
                port=port,
                login=login,
                password=password
            )

            response = self._network.setup_regime_settings(request)

            if response and response.status_code == 200:
                self._error_message = ""
                print("✅ Настройки сохранены")
                # Обновляем данные после сохранения
                self.refresh_settings()
                self.refresh_info()
            else:
                self._error_message = "Ошибка при сохранении настроек"
                self.errorChanged.emit()
                self._is_loading = False
                self.loadingChanged.emit()

        except Exception as e:
            self._error_message = f"Ошибка: {e}"
            self.errorChanged.emit()
            self._is_loading = False
            self.loadingChanged.emit()
            print(f"❌ Ошибка сохранения: {e}")

    def _finish_loading_if_done(self):
        """Завершает загрузку, если оба запроса выполнены"""
        # В реальном коде нужно отслеживать оба запроса
        # Для простоты просто выключаем через таймер
        QTimer.singleShot(1000, self._stop_loading)

    def _stop_loading(self):
        self._is_loading = False
        self.loadingChanged.emit()


class TSPIoTQmlLoader(QMainWindow):
    def __init__(self,
                 window_size: tuple,
                 app_icon_path: str,
                 header_name: str,
                 fonts_path: str,
                 qml_file: str,
                 esm_instance_id: str):
        super().__init__()

        # Создаем контроллер
        self._regime_controller = RegimeController(esm_instance_id)

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
        engine.rootContext().setContextProperty("regimeController", self._regime_controller)
        print("✅ Контроллер зарегистрирован в QML контексте как 'regimeController'")

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
    __WINDOW_SIZE = (450, 350)
    __APP_HEADER_TITLE = "ТС ПИоТ - Контроллер ЛМ ЧЗ"
    __APP_ICON_PATH = os.path.join(SRC_DIR, "ui", "assets", "image_89.png")
    __FONTS_PATH = os.path.join(SRC_DIR, "ui", "fonts")
    __QML_PATH = os.path.join(SRC_DIR, "ui", "regime.qml")
    __ESM_INSTANCE_ID = "00106327428745"  # ID инстанса

    app = QApplication(sys.argv)

    # Создаем и показываем окно
    loader = TSPIoTQmlLoader(
        window_size=__WINDOW_SIZE,
        app_icon_path=__APP_ICON_PATH,
        header_name=__APP_HEADER_TITLE,
        fonts_path=__FONTS_PATH,
        qml_file=__QML_PATH,
        esm_instance_id=__ESM_INSTANCE_ID
    )

    loader.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()