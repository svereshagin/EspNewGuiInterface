import sys
import os

from PySide6.QtWidgets import QApplication
import logging

# Исправленный импорт
from old_src.infrastructure.utils.check_network_gismt import NetworkChecker
from old_src.infrastructure.utils.check_network_gismt import CDNData

print("=== DEBUG INFO ===")
print(f"Python path: {sys.path}")
print(f"Current dir: {os.getcwd()}")
print(f"Frozen: {getattr(sys, 'frozen', False)}")
print(f"MEIPASS: {getattr(sys, '_MEIPASS', None)}")
print("=================")

from old_src.infrastructure.utils.common import check_compile_mode, resource_path
from old_src.infrastructure.utils.qml_loader import MainQmlLoader

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

    # Создаем NetworkChecker
    network_checker = NetworkChecker()

    # Загружаем данные CDN
    try:
        cdn_data = CDNData()

        # Добавляем CDN сервисы для проверки
        network_checker.add_cdn_services(cdn_data.prod_cdns, port=19101)

        # Добавляем сервисы регистрации
        network_checker.add_register_services(
            cdn_data.prod_register_url,
            cdn_data.prod_register_port,
            cdn_data.test_register_url,
            cdn_data.test_register_port
        )

        logger.info("✅ NetworkChecker успешно настроен")
    except Exception as e:
        logger.error(f"❌ Ошибка при настройке NetworkChecker: {e}")
        # Продолжаем работу даже если ошибка

    # Создаем и показываем главное окно
    loader = MainQmlLoader(
        window_size=__WINDOW_SIZE,
        app_icon_path=__APP_ICON_PATH,
        header_name=__APP_HEADER_TITLE,
        fonts_path=__FONTS_PATH,
        qml_file=__QML_PATH,
        use_test_data=use_test_data,
        network_checker=network_checker,  # Передаем network_checker в QML
    )

    def on_about_to_quit():
        logger.info("Приложение закрывается, останавливаю проверку сети...")
        network_checker.stop_periodic_check()

    app.aboutToQuit.connect(on_about_to_quit)

    # Запускаем периодическую проверку после загрузки UI
    network_checker.start_periodic_check(interval_ms=30000)

    loader.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()