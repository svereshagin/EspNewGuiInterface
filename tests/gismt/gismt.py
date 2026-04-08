import sys
import os
import asyncio
import logging
from typing import List, Optional
from concurrent.futures import ThreadPoolExecutor

from PySide6.QtCore import QObject, Slot, Property, Signal, QTimer, QUrl
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QMainWindow
from PySide6.QtQuickWidgets import QQuickWidget
from PySide6.QtGui import QFontDatabase, QIcon

# Импорт сетевого слоя (DTO уже там)
from old_src.network.gismt import GisMtNetwork
from old_src.network.gismt import GisMtSettingsResponseDTO, GisMtSettingsUpdateDTO
from old_src.network.gismt import InstanceResponseDTO, InstancesListResponseDTO

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('gismt_debug.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# ==================== DTO ДЛЯ UI (ТОЛЬКО ДЛЯ ОТОБРАЖЕНИЯ) ====================

class GisMtSettingsInfo:
    """Информация о настройках для отображения в UI"""

    def __init__(self, instance_id: str, compatibility_mode: bool, allow_remote: bool, gismt_address: str):
        self.instance_id = instance_id
        self.compatibility_mode = compatibility_mode
        self.allow_remote = allow_remote
        self.gismt_address = gismt_address

    @classmethod
    def from_response(cls, instance_id: str, response: GisMtSettingsResponseDTO):
        return cls(
            instance_id=instance_id,
            compatibility_mode=response.compatibilityMode,
            allow_remote=response.allowRemoteConnection,
            gismt_address=response.gismtAddress
        )

    def to_dict(self) -> dict:
        return {
            'instanceId': self.instance_id,
            'compatibilityMode': self.compatibility_mode,
            'allowRemote': self.allow_remote,
            'gismtAddress': self.gismt_address
        }


class InstanceInfo:
    """Информация об инстансе для отображения в UI"""

    def __init__(self, id: str, service_state: str, port: int, created_at: Optional[str] = None):
        self.id = id
        self.service_state = service_state
        self.port = port
        self.created_at = created_at

    @classmethod
    def from_dto(cls, dto: InstanceResponseDTO):
        return cls(
            id=dto.id,
            service_state=dto.serviceState,
            port=dto.port,
            created_at=dto.createdAt
        )


# ==================== КОМАНДНЫЙ СЛОЙ ====================

class GisMtCommands:
    """
    Командный слой для работы с ГИС МТ
    Содержит бизнес-логику и может использовать тестовые данные
    """

    def __init__(self, use_test_data: bool = False):
        self._network = GisMtNetwork() if not use_test_data else None
        self._use_test_data = use_test_data
        self._loop = None
        self._executor = ThreadPoolExecutor(max_workers=1)
        logger.info(f"🔧 GisMtCommands инициализирован (test_data={use_test_data})")

    def _get_test_instances(self) -> List[InstanceInfo]:
        """Возвращает тестовые данные для инстансов"""
        return [
            InstanceInfo(
                id="00106327428745",
                service_state="Работает",
                port=8080,
                created_at="2025-01-01T00:00:00"
            ),
            InstanceInfo(
                id="00106327428746",
                service_state="Остановлен",
                port=8081,
                created_at="2025-01-02T00:00:00"
            ),
            InstanceInfo(
                id="00234567890123",
                service_state="Работает",
                port=8082,
                created_at="2025-01-03T00:00:00"
            )
        ]

    def _get_test_settings(self, instance_id: str) -> GisMtSettingsInfo:
        """Возвращает тестовые настройки для инстанса"""
        return GisMtSettingsInfo(
            instance_id=instance_id,
            compatibility_mode=False,
            allow_remote=False,
            gismt_address="https://194.0.209.194:19101"
        )

    def _get_or_create_event_loop(self):
        """Получает или создает event loop"""
        try:
            self._loop = asyncio.get_running_loop()
        except RuntimeError:
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
        return self._loop

    async def _get_instances_async(self) -> List[InstanceInfo]:
        """Асинхронное получение списка инстансов"""
        if self._use_test_data:
            return self._get_test_instances()

        try:
            if not self._network:
                return []

            response = self._network.get_instances()
            if response and response.instances:
                return [InstanceInfo.from_dto(inst) for inst in response.instances]
            return []
        except Exception as e:
            logger.error(f"❌ Ошибка в _get_instances_async: {e}")
            return []

    def get_instances(self) -> List[InstanceInfo]:
        """
        Получает список всех инстансов (синхронная обертка)
        """
        logger.info("🔍 get_instances() вызван")

        try:
            loop = self._get_or_create_event_loop()
            instances = loop.run_until_complete(self._get_instances_async())

            logger.info(f"📋 Получено инстансов: {len(instances)}")
            for inst in instances:
                logger.info(f"  • {inst.id} - {inst.service_state}")

            return instances
        except Exception as e:
            logger.error(f"❌ Ошибка в get_instances: {e}")
            return []

    def get_instance_ids(self) -> List[str]:
        """
        Получает список ID всех инстансов
        """
        instances = self.get_instances()
        return [inst.id for inst in instances]

    def is_instance_registered(self, instance_id: str) -> bool:
        """
        Проверяет, зарегистрирован ли инстанс
        """
        logger.info(f"🔍 Проверка регистрации инстанса: {instance_id}")

        if self._use_test_data:
            # В тестовом режиме считаем, что первый инстанс зарегистрирован
            return instance_id == "00106327428745"

        try:
            instances = self.get_instances()
            is_registered = any(inst.id == instance_id for inst in instances)
            logger.info(f"📊 Инстанс {instance_id} зарегистрирован: {is_registered}")
            return is_registered
        except Exception as e:
            logger.error(f"❌ Ошибка в is_instance_registered: {e}")
            return False

    async def _get_settings_async(self, instance_id: str) -> Optional[GisMtSettingsInfo]:
        """Асинхронное получение настроек"""
        if self._use_test_data:
            return self._get_test_settings(instance_id)

        try:
            if not self._network:
                return None

            response = self._network.get_settings(instance_id)
            if response:
                return GisMtSettingsInfo.from_response(instance_id, response)
            return None
        except Exception as e:
            logger.error(f"❌ Ошибка в _get_settings_async: {e}")
            return None

    def get_settings(self, instance_id: str) -> Optional[GisMtSettingsInfo]:
        """
        Получает настройки драйвера ГИС МТ для указанного инстанса
        """
        logger.info(f"🔍 get_settings для инстанса {instance_id}")

        try:
            loop = self._get_or_create_event_loop()
            settings = loop.run_until_complete(self._get_settings_async(instance_id))

            if settings:
                logger.info(f"✅ Настройки получены для {instance_id}")
            else:
                logger.warning(f"⚠️ Настройки не найдены для {instance_id}")

            return settings
        except Exception as e:
            logger.error(f"❌ Ошибка в get_settings: {e}")
            return None

    async def _update_settings_async(self, instance_id: str,
                                     compatibility_mode: Optional[bool],
                                     allow_remote: Optional[bool],
                                     gismt_address: Optional[str]) -> bool:
        """Асинхронное обновление настроек"""
        if self._use_test_data:
            logger.info("🧪 Тестовый режим: настройки обновлены")
            return True

        try:
            if not self._network:
                return False

            update_dto = GisMtSettingsUpdateDTO(
                compatibilityMode=compatibility_mode,
                allowRemoteConnection=allow_remote,
                gismtAddress=gismt_address
            )

            return self._network.update_settings(instance_id, update_dto)
        except Exception as e:
            logger.error(f"❌ Ошибка в _update_settings_async: {e}")
            return False

    def update_settings(self, instance_id: str,
                        compatibility_mode: Optional[bool] = None,
                        allow_remote: Optional[bool] = None,
                        gismt_address: Optional[str] = None) -> bool:
        """
        Обновляет настройки драйвера ГИС МТ
        """
        logger.info(f"🔧 update_settings для инстанса {instance_id}")

        try:
            loop = self._get_or_create_event_loop()
            result = loop.run_until_complete(
                self._update_settings_async(instance_id, compatibility_mode, allow_remote, gismt_address)
            )

            if result:
                logger.info(f"✅ Настройки обновлены для {instance_id}")
            else:
                logger.error(f"❌ Ошибка обновления настроек для {instance_id}")

            return result
        except Exception as e:
            logger.error(f"❌ Ошибка в update_settings: {e}")
            return False

    async def close_async(self):
        """Асинхронное закрытие соединения"""
        if self._network:
            self._network.close()
            logger.info("🔒 Сетевое соединение закрыто")

    def close(self):
        """Синхронное закрытие соединения"""
        if self._network:
            try:
                loop = self._get_or_create_event_loop()
                if loop.is_running():
                    asyncio.create_task(self.close_async())
                else:
                    loop.run_until_complete(self.close_async())
            except Exception as e:
                logger.error(f"⚠️ Ошибка при закрытии: {e}")

        if self._loop and not self._loop.is_closed():
            self._loop.close()
            self._loop = None

        self._executor.shutdown(wait=False)

    def __del__(self):
        self.close()


# ==================== КОНТРОЛЛЕР ====================

class GisMtController(QObject):
    """
    Контроллер для управления ГИС МТ в QML
    """

    # Сигналы
    instancesListChanged = Signal()
    selectedInstanceChanged = Signal()
    settingsChanged = Signal()
    loadingChanged = Signal()
    errorOccurred = Signal(str)
    operationCompleted = Signal(dict)

    # Сигналы для потоков
    instancesLoaded = Signal(list)
    settingsLoaded = Signal(object)

    def __init__(self, parent=None, use_test_data: bool = False):
        super().__init__(parent)

        self._instances: List[str] = []  # Список ID для ComboBox
        self._instances_info: List[InstanceInfo] = []  # Полная информация
        self._selected_instance: Optional[str] = None
        self._current_settings: Optional[GisMtSettingsInfo] = None
        self._is_loading = False
        self._operation_result: str = ""

        # Командный слой
        self._commands = GisMtCommands(use_test_data=use_test_data)

        # Подключаем сигналы
        self.instancesLoaded.connect(self._on_instances_loaded)
        self.settingsLoaded.connect(self._on_settings_loaded)

        logger.info(f"✅ GisMtController инициализирован (test_data={use_test_data})")

        # Автоматическая загрузка
        QTimer.singleShot(500, self.refresh_instances)

    # Свойства для QML
    @Property(list, notify=instancesListChanged)
    def instances(self):
        """Список ID инстансов для ComboBox"""
        return self._instances

    @Property(str, notify=selectedInstanceChanged)
    def selectedInstance(self):
        return self._selected_instance or ""

    @Property('QVariant', notify=settingsChanged)
    def currentSettings(self):
        """Текущие настройки для отображения"""
        if self._current_settings:
            return self._current_settings.to_dict()
        return None

    @Property(bool, notify=loadingChanged)
    def isLoading(self):
        return self._is_loading

    @Property(str, notify=operationCompleted)
    def operationResult(self):
        return self._operation_result

    # Слоты
    @Slot()
    def refresh_instances(self):
        """Обновляет список инстансов"""
        logger.info("🔄 refresh_instances вызван")

        self._is_loading = True
        self.loadingChanged.emit()

        from threading import Thread
        thread = Thread(target=self._refresh_instances_thread)
        thread.daemon = True
        thread.start()

    def _refresh_instances_thread(self):
        """Выполняется в отдельном потоке"""
        try:
            instances_info = self._commands.get_instances()
            self._instances_info = instances_info
            instance_ids = [inst.id for inst in instances_info]

            logger.info(f"📋 Получено инстансов: {len(instance_ids)}")
            for inst in instances_info:
                logger.info(f"  • {inst.id} - {inst.service_state}")

            # Используем сигнал вместо Q_ARG
            self.instancesLoaded.emit(instance_ids)

        except Exception as e:
            logger.error(f"❌ Ошибка в _refresh_instances_thread: {e}")
            self.errorOccurred.emit(str(e))
            self._is_loading = False
            self.loadingChanged.emit()

    @Slot(list)
    def _on_instances_loaded(self, instance_ids):
        """Слот для обновления UI после загрузки"""
        self._instances = instance_ids
        self.instancesListChanged.emit()
        self._is_loading = False
        self.loadingChanged.emit()

    @Slot(str)
    def select_instance(self, instance_id: str):
        """Выбирает инстанс по ID"""
        logger.info(f"🎯 select_instance({instance_id})")

        if self._selected_instance != instance_id:
            self._selected_instance = instance_id
            self.selectedInstanceChanged.emit()

            # Загружаем настройки
            from threading import Thread
            thread = Thread(target=self._load_settings_thread, args=(instance_id,))
            thread.daemon = True
            thread.start()

    def _load_settings_thread(self, instance_id: str):
        """Загружает настройки в отдельном потоке"""
        try:
            settings = self._commands.get_settings(instance_id)
            # Используем сигнал вместо Q_ARG
            self.settingsLoaded.emit(settings)
        except Exception as e:
            logger.error(f"❌ Ошибка загрузки настроек: {e}")

    @Slot(object)
    def _on_settings_loaded(self, settings):
        """Слот для обновления настроек в UI"""
        self._current_settings = settings
        self.settingsChanged.emit()

        if settings:
            logger.info(f"✅ Настройки загружены для {settings.instance_id}")
        else:
            logger.warning(f"⚠️ Настройки не найдены")

    @Slot()
    def refresh_settings(self):
        """Обновляет настройки текущего инстанса"""
        if self._selected_instance:
            from threading import Thread
            thread = Thread(target=self._load_settings_thread, args=(self._selected_instance,))
            thread.daemon = True
            thread.start()

    @Slot(bool, bool, str)
    def update_settings(self, compatibility_mode: bool, allow_remote: bool, gismt_address: str):
        """Обновляет настройки текущего инстанса"""
        if not self._selected_instance:
            logger.warning("⚠️ Нет выбранного инстанса")
            return

        logger.info(f"📝 Обновление настроек для {self._selected_instance}")

        self._is_loading = True
        self.loadingChanged.emit()

        from threading import Thread
        thread = Thread(target=self._update_settings_thread, args=(
            self._selected_instance,
            compatibility_mode,
            allow_remote,
            gismt_address
        ))
        thread.daemon = True
        thread.start()

    def _update_settings_thread(self, instance_id: str, compatibility_mode: bool,
                                allow_remote: bool, gismt_address: str):
        """Обновляет настройки в отдельном потоке"""
        try:
            success = self._commands.update_settings(
                instance_id=instance_id,
                compatibility_mode=compatibility_mode,
                allow_remote=allow_remote,
                gismt_address=gismt_address
            )

            result = {
                'success': success,
                'message': 'Настройки обновлены' if success else 'Ошибка обновления'
            }

            self._operation_result = result['message']

            # Если успешно, перезагружаем настройки
            if success:
                settings = self._commands.get_settings(instance_id)
                self.settingsLoaded.emit(settings)

            self.operationCompleted.emit(result)

        except Exception as e:
            logger.error(f"❌ Ошибка обновления: {e}")
            self._operation_result = str(e)
            self.operationCompleted.emit({'success': False, 'message': str(e)})
        finally:
            self._is_loading = False
            self.loadingChanged.emit()

    @Slot()
    def clear_selection(self):
        """Сбрасывает выбор"""
        logger.info("🧹 clear_selection()")
        self._selected_instance = None
        self._current_settings = None
        self.selectedInstanceChanged.emit()
        self.settingsChanged.emit()

    def close(self):
        """Закрывает соединения"""
        if self._commands:
            self._commands.close()

    def __del__(self):
        self.close()


# ==================== ЗАГРУЗЧИК QML ====================

class GisMtQmlLoader(QMainWindow):
    def __init__(self,
                 window_size: tuple,
                 app_icon_path: str,
                 header_name: str,
                 fonts_path: str,
                 qml_file: str,
                 use_test_data: bool = False):
        super().__init__()

        # Создаем контроллер
        self._controller = GisMtController(use_test_data=use_test_data)

        # Сохраняем параметры
        self.app_icon_path = app_icon_path
        self.header_name = header_name
        self.window_size = window_size
        self.qml_file = qml_file

        # Загружаем шрифты
        self.__load_fonts(fonts_path)

        # Устанавливаем параметры окна
        self.setWindowTitle(header_name)
        self.setMinimumSize(window_size[0], window_size[1])
        self.resize(window_size[0], window_size[1])
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
        engine.rootContext().setContextProperty("gisMtController", self._controller)
        logger.info("✅ Контроллер зарегистрирован в QML контексте как 'gisMtController'")

        # Загружаем QML из файла
        if os.path.exists(qml_file):
            qml_url = QUrl.fromLocalFile(qml_file)
            logger.info(f"📁 Загрузка QML из: {qml_url.toString()}")
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
        if os.path.exists(self.app_icon_path):
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
        self._controller.close()
        event.accept()


# ==================== ТОЧКА ВХОДА ====================

def main():
    # Параметры
    SRC_DIR = os.path.dirname(os.path.abspath(__file__))
    __WINDOW_SIZE = (700, 650)
    __APP_HEADER_TITLE = "ГИС МТ - Управление настройками"
    __APP_ICON_PATH = os.path.join(SRC_DIR, "ui", "assets", "image_89.png")
    __FONTS_PATH = os.path.join(SRC_DIR, "ui", "fonts")
    __QML_PATH = os.path.join(SRC_DIR, "ui", "GisMtView.qml")
    __USE_TEST_DATA = True  # False для реальных данных

    logger.info("=" * 50)
    logger.info("🚀 ЗАПУСК ПРИЛОЖЕНИЯ ГИС МТ")
    logger.info("=" * 50)
    logger.info(f"📊 Режим тестовых данных: {__USE_TEST_DATA}")

    app = QApplication(sys.argv)

    # Создаем и показываем окно
    loader = GisMtQmlLoader(
        window_size=__WINDOW_SIZE,
        app_icon_path=__APP_ICON_PATH,
        header_name=__APP_HEADER_TITLE,
        fonts_path=__FONTS_PATH,
        qml_file=__QML_PATH,
        use_test_data=__USE_TEST_DATA
    )

    loader.show()

    # Периодическая проверка статуса (каждые 30 секунд)
    def periodic_status_check():
        if loader._controller._selected_instance:
            loader._controller.refresh_settings()
        QTimer.singleShot(30000, periodic_status_check)

    QTimer.singleShot(30000, periodic_status_check)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()