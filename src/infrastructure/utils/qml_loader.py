import os
from PySide6.QtCore import QTimer, QUrl
from PySide6.QtGui import QFontDatabase, QIcon
from PySide6.QtQuickWidgets import QQuickWidget
from PySide6.QtWidgets import QWidget, QVBoxLayout, QMainWindow
import logging
from src.application.application_storage import ApplicationStorage
from .controllers import LMController, GisMtController, KKTController
from src.infrastructure.utils.common import resource_path

logger = logging.getLogger(__name__)


class MainQmlLoader(QMainWindow):
    """Главный загрузчик QML - только UI, без бизнес-логики"""

    def __init__(self,
                 window_size: tuple,
                 header_name: str,
                 qml_file: str,
                 app_icon_path: str = None,
                 fonts_path: str = None,
                 use_test_data: bool = False,
                 mode: bool = False, #разработка vs компиляция
                 ):
        super().__init__()



        # Создаем единое хранилище состояния
        self._storage = ApplicationStorage()

        # Создаем контроллеры (тонкие обертки над storage)
        self._lm_controller = LMController(self._storage)
        self._gismt_controller = GisMtController(self._storage)
        self._kkt_controller = KKTController(self._storage)



        # Сохраняем параметры
        self.app_icon_path = app_icon_path
        self.header_name = header_name
        self.window_size = window_size
        self.qml_file = qml_file

        # Загружаем шрифты
        if fonts_path:
            self.__load_fonts(fonts_path)
        if app_icon_path:
            self.__set_app_icon()

        # Устанавливаем параметры окна
        self.setWindowTitle(header_name)
        self.setMinimumSize(window_size[0], window_size[1])
        self.resize(window_size[0], window_size[1])

        # Создаем центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        # Создаем QQuickWidget
        self.quick_widget = QQuickWidget()
        engine = self.quick_widget.engine()

        # Регистрируем storage и контроллеры в контексте QML
        engine.rootContext().setContextProperty("appStorage", self._storage)
        engine.rootContext().setContextProperty("lmController", self._lm_controller)
        engine.rootContext().setContextProperty("gisMtController", self._gismt_controller)
        engine.rootContext().setContextProperty("kktController", self._kkt_controller)

        logger.info("✅ Storage и контроллеры зарегистрированы в QML контексте")

        # Загружаем QML
        if qml_file.startswith("qrc:"):
            qml_url = QUrl(qml_file)
            logger.info(f"📦 Загрузка QML из ресурсов: {qml_url.toString()}")
            self.quick_widget.setSource(qml_url)
        elif os.path.exists(qml_file):
            qml_url = QUrl.fromLocalFile(qml_file)
            logger.info(f"📁 Загрузка QML из файла: {qml_url.toString()}")
            self.quick_widget.setSource(qml_url)
        else:
            logger.error(f"❌ QML файл не найден: {qml_file}")
        # Проверка ошибок
        if self.quick_widget.status() == QQuickWidget.Status.Error:
            logger.error("❌ Ошибка загрузки QML:")
            for error in self.quick_widget.errors():
                logger.error(f"   {error.toString()}")
        else:
            logger.info("✅ QML успешно загружен")


        layout.addWidget(self.quick_widget)


    def __set_app_icon(self):
        if self.app_icon_path.startswith("qrc:"):
            self.setWindowIcon(QIcon(self.app_icon_path))
            logger.info(f"✅ Иконка загружена из ресурсов: {self.app_icon_path}")
        elif os.path.exists(self.app_icon_path):
            self.setWindowIcon(QIcon(self.app_icon_path))
            logger.info(f"✅ Иконка загружена: {self.app_icon_path}")
        else:
            logger.warning(f"❌ Иконка не найдена: {self.app_icon_path}")


    def __load_fonts(self, fonts_dir):
        if not os.path.exists(fonts_dir):
            logger.warning(f"❌ Папка со шрифтами не найдена: {fonts_dir}")
            return

        logger.info(f"📁 Загружаем шрифты из: {fonts_dir}")
        for font_file in os.listdir(fonts_dir):
            if font_file.endswith(('.ttf', '.otf', '.ttc')):
                font_path = os.path.join(fonts_dir, font_file)
                font_id = QFontDatabase.addApplicationFont(font_path)
                if font_id != -1:
                    font_families = QFontDatabase.applicationFontFamilies(font_id)
                    logger.info(f"  ✅ Загружен: {font_file} -> {font_families}")



    def closeEvent(self, event):
        """Обработка закрытия окна"""
        logger.info("🔒 Закрытие приложения")
        if hasattr(self, '_storage'):
            self._storage.close()
        event.accept()