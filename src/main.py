import os
import sys
from PySide6.QtWidgets import QApplication

from src.core.config import Settings
from src.infrastructure.utils.common import resolve_path
from src.infrastructure.utils.qml_loader import TSPIoTQmlLoader

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

__WINDOW_SIZE = (829, 612)
__APP_ICON_PATH = "../ui/assets/image_89.png"
__APP_HEADER_TITLE = "ТС ПИоТ"
__FONTS_PATH = "../ui/fonts"
__QML_PATH = "../ui/Gadget.ui.qml"

def check_compile_mode():
    """Проверяет аргументы командной строки для режима компиляции"""
    if '--compiled' in sys.argv:
        # Удаляем аргумент, чтобы он не мешал QApplication
        sys.argv.remove('--compiled')
        return True
    elif '--dev' in sys.argv:
        sys.argv.remove('--dev')
        return False
    return False  # по умолчанию режим разработки


if __name__ == "__main__":
    use_compiled = check_compile_mode()
    print(f"🔧 Режим компиляции: {use_compiled}")

    app = QApplication(sys.argv)

    settings = Settings()

    # Конфигурируем
    if settings.initialize():
        # Получаем порт и URL
        port = settings.get_port()
        url = settings.get_orchestrator_url()

        # Выводим информацию
        print(f"✅ Оркестратор доступен по адресу: {url}")
        print(f"📁 Директория конфигурации: {settings.get_config_dir()}")
        print(f"📄 Файл настроек: {settings.get_settings_file()}")
        print(f"📝 Файл лога: {settings.get_log_file()}")
        print(f"🌐 URL оркестратора: {settings.get_orchestrator_url()}")

    # Разрешаем пути для ресурсов
    icon_path = resolve_path(__APP_ICON_PATH)
    fonts_path = resolve_path(__FONTS_PATH)
    qml_path = resolve_path(__QML_PATH)


    tspiot = TSPIoTQmlLoader(
        window_size=__WINDOW_SIZE,
         app_icon_path=__APP_ICON_PATH,
         header_name=__APP_HEADER_TITLE,
         fonts_path=__FONTS_PATH,
        use_compiled_resources=use_compiled,
        qml_file=__QML_PATH,
    )
    tspiot.show()
    sys.exit(app.exec())