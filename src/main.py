import sys
import os
from PySide6.QtWidgets import QApplication
import logging

from infrastructure.utils.common import check_compile_mode, resource_path
from infrastructure.utils.qml_loader import MainQmlLoader

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    use_compiled = check_compile_mode()
    use_test_data = False

    __WINDOW_SIZE = (900, 700)
    __APP_HEADER_TITLE = "Управление кассами и интеграциями"

    logger.info("=" * 50)
    logger.info("ЗАПУСК ГЛАВНОГО ПРИЛОЖЕНИЯ")
    logger.info("=" * 50)
    logger.info(f"🔧 Режим компиляции: {use_compiled}")
    logger.info(f"📊 Режим тестовых данных: {use_test_data}")

    # Пути для разработки и для скомпилированной версии
    __APP_ICON_PATH = resource_path(os.path.join("ui", "assets", "image_89.png"))
    __FONTS_PATH = resource_path(os.path.join("ui", "fonts"))
    __QML_PATH = resource_path(os.path.join("ui", "MainView.qml"))

    # Проверяем существование файлов
    logger.info(f"📁 Проверка QML файла: {__QML_PATH} существует? {os.path.exists(__QML_PATH)}")
    logger.info(f"📁 Проверка папки со шрифтами: {__FONTS_PATH} существует? {os.path.exists(__FONTS_PATH)}")
    logger.info(f"📁 Проверка иконки: {__APP_ICON_PATH} существует? {os.path.exists(__APP_ICON_PATH)}")

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