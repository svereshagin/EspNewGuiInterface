import os
from time import strftime, localtime
from typing import Optional, List

from PySide6.QtQml import QQmlEngine
from PySide6.QtQuickWidgets import QQuickWidget
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from PySide6.QtCore import QUrl, QObject, Property, QTimer, Slot, Signal, QMutex, QWaitCondition, QThread
from PySide6.QtGui import QFontDatabase, QIcon

from src.application.kkt_controller import KKTController

from src.application.kkt_controller import KKTCommand


class KKTWorker(QObject):
    """
    Рабочий класс для выполнения запросов в отдельном потоке
    """

    # Сигналы
    finished = Signal(object)  # Сигнал с результатом (список серийных номеров)
    error = Signal(str)  # Сигнал с ошибкой

    def __init__(self):
        super().__init__()
        print("🔧 KKTWorker инициализирован")
        self._kkt_command = KKTCommand()
        self._mutex = QMutex()
        self._condition = QWaitCondition()
        self._is_running = True

    @Slot()
    def process(self):
        """
        Основной метод, выполняемый в потоке
        """
        print("🔄 KKTWorker.process() запущен в потоке")

        try:
            # Выполняем запрос
            result = self._kkt_command.get_kkt_list()

            # Отправляем результат в главный поток
            self.finished.emit(result)

        except Exception as e:
            print(f"❌ Ошибка в KKTWorker: {e}")
            self.error.emit(str(e))

    @Slot()
    def stop(self):
        """
        Останавливает работу worker'а
        """
        self._is_running = False
        self._condition.wakeAll()


class KKTController(QObject):
    """
    Контроллер для управления кассами с асинхронными запросами
    """

    # Сигналы для обновления UI
    kktListChanged = Signal()
    selectedKktChanged = Signal()
    loadingChanged = Signal()
    initializedChanged = Signal()
    errorOccurred = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        print("✅ KKTController инициализирован")

        # Данные
        self._kkt_list: List[str] = []
        self._selected_kkt: str = ""
        self._is_loading: bool = False
        self._is_initialized: bool = False

        # Для потоков
        self._thread: Optional[QThread] = None
        self._worker: Optional[KKTWorker] = None
        self._pending_request: bool = False

        # Таймер для отложенной загрузки (UI покажется сначала)
        self._init_timer = QTimer()
        self._init_timer.setSingleShot(True)
        self._init_timer.timeout.connect(self._initial_load)
        self._init_timer.start(300)  # 300 мс задержка для показа UI

        print("⏱ Таймер инициализации запущен на 300мс")

    def _initial_load(self):
        """Первоначальная загрузка данных после показа UI"""
        print("🚀 Начальная загрузка данных...")
        self.refresh_kkt_list()

    @Property(list, notify=kktListChanged)
    def kktList(self):
        """Возвращает список серийных номеров касс"""
        return self._kkt_list

    @Property(str, notify=selectedKktChanged)
    def selectedKkt(self):
        """Возвращает выбранный серийный номер"""
        return self._selected_kkt

    @Property(bool, notify=loadingChanged)
    def isLoading(self):
        """Флаг загрузки"""
        return self._is_loading

    @Property(bool, notify=initializedChanged)
    def isInitialized(self):
        """Флаг, что контроллер инициализирован"""
        return self._is_initialized

    @Slot()
    def refresh_kkt_list(self):
        """
        Обновляет список касс асинхронно
        """
        if self._is_loading:
            print("⚠️ Загрузка уже выполняется, запрос проигнорирован")
            return

        print("🔄 refresh_kkt_list вызван (асинхронный режим)")

        self._is_loading = True
        self.loadingChanged.emit()

        # Останавливаем существующий поток, если он есть
        self._stop_current_thread()

        # Создаем новый поток и worker
        self._create_and_start_thread()

    def _stop_current_thread(self):
        """Останавливает текущий поток, если он существует"""
        if self._thread and self._thread.isRunning():
            print("⏹ Останавливаем текущий поток...")

            # Останавливаем worker
            if self._worker:
                self._worker.stop()

            # Завершаем поток
            self._thread.quit()
            self._thread.wait(1000)  # Ждем максимум 1 секунду

            if self._thread.isRunning():
                print("⚠️ Поток не остановился, принудительно завершаем")
                self._thread.terminate()
                self._thread.wait()

    def _create_and_start_thread(self):
        """Создает и запускает новый поток с worker'ом"""

        # Создаем поток
        self._thread = QThread()

        # Создаем worker (без родителя, чтобы можно было переместить в поток)
        self._worker = KKTWorker()
        self._worker.moveToThread(self._thread)

        # Подключаем сигналы
        self._thread.started.connect(self._worker.process)
        self._worker.finished.connect(self._on_request_finished)
        self._worker.error.connect(self._on_request_error)
        self._worker.finished.connect(self._cleanup_thread)
        self._worker.error.connect(self._cleanup_thread)

        # Запускаем поток
        print("▶ Запуск потока для запроса...")
        self._thread.start()

    def _cleanup_thread(self):
        """Очищает ресурсы потока после завершения"""
        if self._thread and self._thread.isRunning():
            print("🧹 Очистка потока...")
            self._thread.quit()
            self._thread.wait(1000)

            # Удаляем объекты
            if self._worker:
                self._worker.deleteLater()
                self._worker = None

            self._thread.deleteLater()
            self._thread = None

    def _on_request_finished(self, result):
        """
        Обработка успешного результата запроса
        """
        print(f"✅ Запрос завершен успешно, получено {len(result)} элементов")

        # Обновляем список
        self._kkt_list = result
        self._is_initialized = True

        # Отправляем сигналы
        self.kktListChanged.emit()
        self.initializedChanged.emit()

        print(f"📋 Новый список: {self._kkt_list}")

        # Сбрасываем флаг загрузки
        self._is_loading = False
        self.loadingChanged.emit()

    def _on_request_error(self, error_msg):
        """
        Обработка ошибки запроса
        """
        print(f"❌ Ошибка запроса: {error_msg}")

        # Очищаем список
        self._kkt_list = []
        self._is_initialized = True  # Всегда помечаем как инициализированный

        # Отправляем сигналы
        self.kktListChanged.emit()
        self.initializedChanged.emit()
        self.errorOccurred.emit(f"Ошибка загрузки: {error_msg}")

        # Сбрасываем флаг загрузки
        self._is_loading = False
        self.loadingChanged.emit()

    @Slot(str)
    def select_kkt(self, kkt_serial: str):
        """Выбирает кассу по серийному номеру"""
        print(f"🎯 select_kkt({kkt_serial})")

        if self._selected_kkt != kkt_serial:
            self._selected_kkt = kkt_serial
            self.selectedKktChanged.emit()
            print(f"✅ Выбран серийный номер: {kkt_serial}")

    @Slot()
    def clear_selection(self):
        """Сбрасывает выбор"""
        print("🧹 clear_selection()")

        self._selected_kkt = ""
        self.selectedKktChanged.emit()

    @Slot(str, result=str)
    def get_kkt_status(self, kkt_serial: str) -> str:
        """Возвращает статус кассы"""
        if kkt_serial in self._kkt_list:
            return "🟢 Доступна"
        elif kkt_serial:
            return "🟡 Не в списке"
        return "⚪ Не выбрана"

    def __del__(self):
        """Деструктор для очистки ресурсов"""
        print("🧹 Очистка KKTController")
        self._stop_current_thread()


class TSPIoTQmlLoader(QMainWindow):
    __BASE_RESOURCE_QML_NAME = "MainView.qml"

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
        self._kkt_controller = KKTController()

        # Сохраняем параметры
        self.app_icon_path = app_icon_path
        self.header_name = header_name
        self.window_size = window_size
        self.qml_base_file = qml_file

        # Загружаем шрифты
        self.__load_fonts(fonts_path)

        # Устанавливаем параметры окна
        self.setWindowTitle(header_name)
        self.setFixedSize(window_size[0], window_size[1])
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
        engine.rootContext().setContextProperty("kktController", self._kkt_controller)
        print("✅ Контроллер зарегистрирован в QML контексте как 'kktController'")

        # Загружаем QML
        qml_url = QUrl.fromLocalFile(qml_file)
        print(f"📁 Загрузка QML из: {qml_url.toString()}")

        self.quick_widget.setSource(qml_url)

        # Проверка ошибок
        if self.quick_widget.status() == QQuickWidget.Status.Error:
            print("❌ Ошибка загрузки QML:")
            for error in self.quick_widget.errors():
                print(f"   {error.toString()}")
        else:
            print("✅ QML успешно загружен")

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
                    ":/MainView.qml",
                    ":/ui/MainView.qml",
                    ":/src/ui/MainView.qml",
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