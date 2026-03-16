import os
import sys
from PySide6.QtWidgets import QApplication

from src.core.config import Settings
from src.infrastructure.utils.common import resolve_path
from src.infrastructure.utils.qml_loader import TSPIoTQmlLoader

# Добавляем корень проекта в sys.path (если ещё не добавлен)
SRC_DIR = os.path.dirname(os.path.abspath(__file__))

__WINDOW_SIZE = (829, 612)
__APP_HEADER_TITLE = "ТС ПИоТ"

# Вариант А — абсолютные пути от src/
__APP_ICON_PATH = os.path.join(SRC_DIR, "ui", "assets", "image_89.png")
__FONTS_PATH    = os.path.join(SRC_DIR, "ui", "fonts")
__QML_PATH      = os.path.join(SRC_DIR, "ui", "Gadget.ui.qml")       # ← теперь от корня

def check_compile_mode():
    if '--compiled' in sys.argv:
        sys.argv.remove('--compiled')
        return True
    if '--dev' in sys.argv:
        sys.argv.remove('--dev')
        return False
    return False

if __name__ == "__main__":
    use_compiled = check_compile_mode()
    print(f"🔧 Режим компиляции: {use_compiled}")

    app = QApplication(sys.argv)

    settings = Settings()
    if settings.initialize():
        port = settings.get_port()
        url = settings.get_orchestrator_url()
        print(f"✅ Оркестратор доступен по адресу: {url}")
        print(f"📁 Директория конфигурации: {settings.get_config_dir()}")
        # ... остальные print'ы

    # Пути теперь относительные от корня проекта
    icon_path = resolve_path(__APP_ICON_PATH)
    fonts_path = resolve_path(__FONTS_PATH)
    qml_path = resolve_path(__QML_PATH)

    print(f"Icon resolved: {icon_path}")
    print(f"Fonts dir resolved: {fonts_path}")
    print(f"QML resolved: {qml_path}")

    tspiot = TSPIoTQmlLoader(
        window_size=__WINDOW_SIZE,
        app_icon_path=icon_path,          # ← лучше передавать уже разрешённый путь
        header_name=__APP_HEADER_TITLE,
        fonts_path=fonts_path,
        use_compiled_resources=use_compiled,
        qml_file=qml_path,                # ← в dev-режиме это будет абсолютный путь к ui/Gadget.ui.qml
    )
    tspiot.show()
    sys.exit(app.exec())