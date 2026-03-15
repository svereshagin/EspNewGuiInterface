import os

from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from PySide6.QtCore import QUrl
from PySide6.QtQuickWidgets import QQuickWidget
from PySide6.QtGui import QFontDatabase, QIcon





class TSPIoTQmlLoader(QMainWindow):

    __BASE_RESOURCE_QML_NAME = "base.qml"

    def __init__(self,
                 window_size: tuple,
                 app_icon_path: str,
                 header_name: str,
                 fonts_path: str,
                 use_compiled_resources: bool,
                 qml_file: str
                 ):
        """
        Args:
            fonts_path: Путь к папке со шрифтами.
                       Если None - шрифты не загружаются
        """
        super().__init__()


        self.app_icon_path = app_icon_path
        self.header_name = header_name
        self.window_size = window_size
        self.use_compiled_resources = use_compiled_resources
        self.qml_base_file = qml_file  # "Gadget.ui.qml" <- основной qml файл


        #подгружаем стили
        self.__load_fonts(fonts_path)

        #запрещаем растягивание окна
        self.setFixedSize(window_size[0], window_size[1])

        self.__set_header()
        self.__set_app_icon()
        self.__load_qml_file()


    def __set_app_icon(self):
        icon_path = os.path.abspath(self.app_icon_path)
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
            print(f"Иконка загружена: {icon_path}")
        else:
            print(f"Иконка не найдена: {icon_path}")

    def __set_header(self):
        self.setWindowTitle(self.header_name)


    def __load_fonts(self, fonts_dir):
        """Загружает шрифты из указанной директории"""
        if not os.path.exists(fonts_dir):
            print(f"Папка со шрифтами не найдена: {fonts_dir}")
            return

        print(f"Загружаем шрифты из: {fonts_dir}")
        for font_file in os.listdir(fonts_dir):
            if font_file.endswith(('.ttf', '.otf', '.ttc')):
                font_path = os.path.join(fonts_dir, font_file)
                font_id = QFontDatabase.addApplicationFont(font_path)
                if font_id != -1:
                    font_families = QFontDatabase.applicationFontFamilies(font_id)
                    print(f"  Загружен: {font_file} -> {font_families}")
                else:
                    print(f"  Ошибка загрузки: {font_file}")


    def __load_qml_file(self):
        """Загружает QML файл"""
        # Создаем центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Создаем layout
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)  # Убираем отступы

        # Создаем виджет для QML
        self.quick_widget = QQuickWidget()

        # Получаем URL для загрузки
        qml_url = self.__get_qml_url()
        print(f"📁 Загрузка QML из: {qml_url.toString()}")

        # Загружаем QML
        self.quick_widget.setSource(qml_url)

        # Добавляем в layout
        layout.addWidget(self.quick_widget)

        # Проверка ошибок
        if self.quick_widget.status() != QQuickWidget.Status.Ready:
            print("❌ Ошибка загрузки QML:")
            for error in self.quick_widget.errors():
                print(f"   {error.toString()}")
        else:
            print("✅ QML успешно загружен")


    def __get_qml_url(self):
        """Определяет URL для загрузки QML"""
        if self.use_compiled_resources:
            # РЕЖИМ 1: Из скомпилированных ресурсов
            try:
                import resources_rc
                print("📦 Ресурсы загружены из памяти")
                return QUrl(f"qrc:/{self.__BASE_RESOURCE_QML_NAME}")
            except ImportError:
                print("Ресурсы не скомпилированы, видимо путь проброшен неверно")
            # РЕЖИМ 2: Из QML файла напрямую
        else:
            return QUrl.fromLocalFile(self.qml_base_file)

