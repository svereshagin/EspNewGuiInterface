import sys
import os


from PySide6.QtWidgets import QApplication
import logging


print("=== DEBUG INFO ===")
print(f"Python path: {sys.path}")
print(f"Current dir: {os.getcwd()}")
print(f"Frozen: {getattr(sys, 'frozen', False)}")
print(f"MEIPASS: {getattr(sys, '_MEIPASS', None)}")
print("=================")

from src.infrastructure.utils.common import check_compile_mode, resource_path
from src.infrastructure.utils.qml_loader import MainQmlLoader

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)





def main():
    use_compiled = getattr(sys, 'frozen', False)
    if use_compiled:
        import ui.resources_rc

    use_test_data = False

    __WINDOW_SIZE = (900, 700)
    __APP_HEADER_TITLE = "Управление кассами и интеграциями"

    logger.info("=" * 50)
    logger.info("ЗАПУСК ГЛАВНОГО ПРИЛОЖЕНИЯ")
    logger.info("=" * 50)
    logger.info(f"🔧 Режим компиляции: {use_compiled}")
    logger.info(f"📊 Режим тестовых данных: {use_test_data}")

    # Пути для разработки и для скомпилированной версии

    if use_compiled:
        __QML_PATH = "qrc:/MainView.qml"
        __APP_ICON_PATH = "qrc:/assets/image_89.png"
        __FONTS_PATH = None  # шрифты тоже должны быть в qrc или None
    else:
        __APP_ICON_PATH = resource_path(os.path.join("ui", "assets", "image_89.png"))
        __FONTS_PATH = resource_path(os.path.join("ui", "fonts"))
        __QML_PATH = resource_path(os.path.join("ui", "MainView.qml"))

    if use_compiled:
        logger.info(f"📦 QML: {__QML_PATH}")
        logger.info(f"📦 Иконка: {__APP_ICON_PATH}")
        logger.info(f"📦 Шрифты: {__FONTS_PATH}")
    else:
        logger.info(f"📁 QML существует? {os.path.exists(__QML_PATH)}")
        logger.info(f"📁 Шрифты существует? {os.path.exists(__FONTS_PATH)}")
        logger.info(f"📁 Иконка существует? {os.path.exists(__APP_ICON_PATH)}")

    app = QApplication(sys.argv)

    # Создаем и показываем главное окно
    loader = MainQmlLoader(
        window_size=__WINDOW_SIZE,
        app_icon_path=__APP_ICON_PATH,
        header_name=__APP_HEADER_TITLE,
        fonts_path=__FONTS_PATH,
        qml_file=__QML_PATH,
        use_test_data=use_test_data,
    )

    loader.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()