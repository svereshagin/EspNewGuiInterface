import os
from time import strftime, localtime

from PySide6.QtQml import QQmlEngine
from PySide6.QtQuickWidgets import QQuickWidget
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from PySide6.QtCore import QUrl, QObject, Property, QTimer
from PySide6.QtGui import QFontDatabase, QIcon

from application.kkt_controller import KKTController


class KKTControllerQML(QObject):
    """Основной backend класс для связи с QML"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._kkt_controller = KKTController()

    @Property(QObject, constant=True)
    def kktController(self):
        return self._kkt_controller


class TSPIoTQmlLoader(QMainWindow):
    __BASE_RESOURCE_QML_NAME = "Gadget.ui.qml"

    def __init__(self,
                 window_size: tuple,
                 app_icon_path: str,
                 header_name: str,
                 fonts_path: str,
                 use_compiled_resources: bool,
                 qml_file: str
                 ):
        super().__init__()

        # Создаем контроллер
        self.__kkt_controller_qml = KKTControllerQML()
        self._kkt_controller = self.__kkt_controller_qml.kktController

        # Сохраняем параметры
        self.app_icon_path = app_icon_path
        self.header_name = header_name
        self.window_size = window_size
        self.use_compiled_resources = use_compiled_resources
        self.qml_base_file = qml_file

        # Подгружаем шрифты
        self.__load_fonts(fonts_path)

        # Устанавливаем заголовок и иконку
        self.__set_header()
        self.__set_app_icon()

        # Устанавливаем размер окна
        self.setFixedSize(window_size[0], window_size[1])

        # Создаем центральный виджет и layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        # СОЗДАЕМ QQuickWidget
        self.quick_widget = QQuickWidget()

        # Получаем движок QML из QQuickWidget и регистрируем контроллер
        engine = self.quick_widget.engine()
        engine.rootContext().setContextProperty("kktController", self._kkt_controller)
        print("✅ Контроллер зарегистрирован в QML контексте как 'kktController'")

        # Получаем URL для загрузки
        qml_url = self.__get_qml_url()

        if qml_url.isEmpty():
            print("❌ Не удалось получить URL для загрузки QML")
            return

        print(f"📁 Загрузка QML из: {qml_url.toString()}")

        # Загружаем QML
        self.quick_widget.setSource(qml_url)

        # Проверяем ошибки
        if self.quick_widget.status() == QQuickWidget.Status.Error:
            print("❌ Ошибка загрузки QML:")
            for error in self.quick_widget.errors():
                print(f"   {error.toString()}")
        else:
            print("✅ QML успешно загружен")

            # ДАЕМ ВРЕМЯ НА ИНИЦИАЛИЗАЦИЮ QML
            QTimer.singleShot(200, self._setup_qml_after_load)

        # Добавляем QQuickWidget в layout
        layout.addWidget(self.quick_widget)

    def _setup_qml_after_load(self):
        """Настройка QML после полной загрузки"""
        print("⏱ Выполняем настройку QML после задержки...")

        # Устанавливаем время
        curr_time = strftime("%H:%M:%S", localtime())
        root_object = self.quick_widget.rootObject()

        if root_object:
            root_object.setProperty('currTime', curr_time)
            print(f"⏰ Установлено время: {curr_time}")

            # Вызываем метод загрузки списка, если он есть
            if hasattr(root_object, 'loadKktList'):
                print("📞 Вызываем loadKktList() из QML")
                root_object.loadKktList()
            elif hasattr(root_object, 'refreshKktList'):
                print("📞 Вызываем refreshKktList() из QML")
                root_object.refreshKktList()
            else:
                print("⚠️ Методы loadKktList/refreshKktList не найдены в QML")

    def __set_app_icon(self):
        icon_path = os.path.abspath(self.app_icon_path)
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
            print(f"✅ Иконка загружена: {icon_path}")
        else:
            print(f"❌ Иконка не найдена: {icon_path}")

    def __set_header(self):
        self.setWindowTitle(self.header_name)

    def __load_fonts(self, fonts_dir):
        """Загружает шрифты из указанной директории"""
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
                else:
                    print(f"  ❌ Ошибка загрузки: {font_file}")

    def __get_qml_url(self):
        """Определяет URL для загрузки QML"""
        if self.use_compiled_resources:
            try:
                import src.resources_rc
                print("📦 Ресурсы успешно загружены из памяти")

                from PySide6.QtCore import QFile

                possible_paths = [
                    ":/Gadget.ui.qml",
                    ":/ui/Gadget.ui.qml",
                    ":/src/ui/Gadget.ui.qml",
                    f":/{self.__BASE_RESOURCE_QML_NAME}"
                ]

                for path in possible_paths:
                    if QFile.exists(path):
                        print(f"✅ Файл найден как {path}")
                        return QUrl(path)

                print("❌ Файл не найден в ресурсах")

            except ImportError as e:
                print(f"❌ Ошибка импорта ресурсов: {e}")

        # Файловая система
        if os.path.exists(self.qml_base_file):
            print(f"📁 Загружаем из файла: {self.qml_base_file}")
            return QUrl.fromLocalFile(self.qml_base_file)

        return QUrl()