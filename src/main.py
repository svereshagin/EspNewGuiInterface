import sys
import os

# Настройка логгирования QML [ДО ЛЮБЫХ ИМПОРТОВ]
os.environ["QT_LOGGING_RULES"] = (
    "*.debug=false;"
    "*.info=false;"
    "qt.scenegraph.*=false;"
    "qt.quick.*=false;"
    "qt.qml.binding=false;"
    "qt.qml.compiler=false;"
    "qt.qml.diskcache=false;"
    "qt.qml.gc=false;"
    # только нужное
    "qml=true;"
    "js=true;"
    "qt.qml.context=true"
)
os.environ["QT_MESSAGE_PATTERN"] = "[%{type}] %{message}"

from pathlib import Path
from PySide6.QtCore import qInstallMessageHandler, QtMsgType, QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

sys.path.insert(0, str(Path(__file__).parent))

from src.services.kkt_service import KKTService
from src.services.tspiot import TSPIoTService
from src.storage.application_storage import AppStorage



try:
    from src.ui.whitelabel import resources_rc
except ImportError:
    # Если не скомпилированы, пробуем локальный импорт
    try:
        import resources_rc
    except ImportError:
        print("⚠️ Resources not compiled, will use filesystem")




# Системный шум, который может просочиться сквозь rules
_NOISE = (
    "(RT)", "syncAndRender", "QQuickWindowPrivate",
    "atlastexture", "QSGNode", "time in renderer",
    "[rub]", "[window", "unlock after sync",
    "Frame prepared", "done drawing", "processEvents",
    "sceneGraphChanged", "waking Gui", "rendering",
)


def qt_message_handler(msg_type, context, message):
    msg = message if isinstance(message, str) else message.toString()

    if any(noise in msg for noise in _NOISE):
        return

    file = getattr(context, 'file', '') or ''
    line = getattr(context, 'line', 0) or 0

    prefix_map = {
        QtMsgType.QtDebugMsg:    "🐛 [DEBUG]",
        QtMsgType.QtInfoMsg:     "ℹ️  [INFO]",
        QtMsgType.QtWarningMsg:  "⚠️  [WARN]",
        QtMsgType.QtCriticalMsg: "❌ [CRIT]",
        QtMsgType.QtFatalMsg:    "💀 [FATAL]",
    }
    prefix = prefix_map.get(msg_type, "[???]")
    location = f" ({os.path.basename(file)}:{line})" if file else ""
    print(f"{prefix}{location} {msg}", flush=True)


def get_resource_path() -> str:
    if hasattr(sys, "_MEIPASS"):
        base = sys._MEIPASS
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, "ui/whitelabel/main.qml")


def main():
    qInstallMessageHandler(qt_message_handler)

    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    engine.warnings.connect(
        lambda warnings: [print(f"⚠️ QML WARNING: {w.toString()}", flush=True) for w in warnings]
    )

    kkt_service = KKTService()
    tspiot_service = TSPIoTService()
    app_storage = AppStorage(
        kkt_service=kkt_service,
        tspiot_service=tspiot_service,
        cache_ttl_seconds=300,
        is_test=False
    )

    engine.rootContext().setContextProperty("AppStorage", app_storage)

    qml_file = get_resource_path()
    print(f"ℹ️  QML path: {qml_file}", flush=True)
    print(f"ℹ️  File exists: {os.path.exists(qml_file)}", flush=True)

    if hasattr(sys, "_MEIPASS"):
        # Скомпилированный билд — грузим из ресурсов
        qml_url = QUrl("qrc:/main.qml")
        print("ℹ️  Loading from resources: qrc:/main.qml", flush=True)
    else:
        # Разработка — грузим с диска
        qml_file = get_resource_path()
        print(f"ℹ️  QML path: {qml_file}", flush=True)
        print(f"ℹ️  File exists: {os.path.exists(qml_file)}", flush=True)
        qml_url = QUrl.fromLocalFile(os.path.abspath(qml_file))
    print("loading", qml_url)
    engine.load(qml_url)

    if not engine.rootObjects():
        print("💀 FAILED: no root objects", flush=True)
        sys.exit(-1)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()