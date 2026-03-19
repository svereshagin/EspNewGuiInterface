import sys
import os
import asyncio
from typing import List, Optional
from concurrent.futures import ThreadPoolExecutor
from PySide6.QtCore import QObject, Slot, Property, Signal, QTimer, QUrl
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QMainWindow
from PySide6.QtQuickWidgets import QQuickWidget
from PySide6.QtGui import QFontDatabase, QIcon

from src.domain.kkt.entity import CashInfo, ShiftState, KktInfo
from src.network.kkt import KKTNetwork


class KKTCommand:
    """Класс для работы с сетью - возвращает данные от API"""

    def __init__(self,  use_test_data=True):
        self._cached_result = None
        self._network = None
        self._loop = None
        self._executor = ThreadPoolExecutor(max_workers=1)
        self._use_test_data = use_test_data  # ИЗМЕНЕНИЕ 2: сохранить флаг
        print("🔧 KKTCommand инициализирован")

    def _get_test_data(self) -> CashInfo:
        """Возвращает тестовые данные"""
        print("🧪 Используем тестовые данные")
        return CashInfo(
            kkt=[
                KktInfo(
                    kktSerial='00106327428745',
                    fnSerial='9999078902018941',
                    kktInn='9717169631',
                    kktRnm='0000000001040014',
                    modelName='АТОЛ FPrint-22ПТК',
                    dkktVersion='10.10.8.23',
                    developer='АТОЛ',
                    manufacturer='АТОЛ',
                    shiftState=ShiftState.CLOSED
                ),
                KktInfo(
                    kktSerial='00106327428746',
                    fnSerial='9999078902018942',
                    kktInn='7712345678',
                    kktRnm='0000000001040015',
                    modelName='АТОЛ FPrint-55ПТК',
                    dkktVersion='10.12.5.11',
                    developer='АТОЛ',
                    manufacturer='АТОЛ',
                    shiftState=ShiftState.OPENED
                ),
                KktInfo(
                    kktSerial='00234567890123',
                    fnSerial='8888123456789012',
                    kktInn='7722334455',
                    kktRnm='0000000001040016',
                    modelName='ШТРИХ-М-01Ф',
                    dkktVersion='5.2.3.1',
                    developer='ШТРИХ-М',
                    manufacturer='ШТРИХ-М',
                    shiftState=ShiftState.CLOSED
                )
            ]
        )

    def _get_network(self):
        """Получает или создает экземпляр KKTNetwork (синглтон)"""
        if self._use_test_data:  # ИЗМЕНЕНИЕ 3: не создаем сеть для тестов
            return None
        if self._network is None:
            self._network = KKTNetwork()
        return self._network

    def _get_or_create_event_loop(self):
        """Получает или создает event loop"""
        try:
            self._loop = asyncio.get_running_loop()
        except RuntimeError:
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
        return self._loop

    async def _get_kkt_list_async(self) -> Optional[CashInfo]:
        """Асинхронное получение списка касс"""
        if self._use_test_data:  # ИЗМЕНЕНИЕ 4: возвращаем тестовые данные
            return self._get_test_data()
        try:
            network = self._get_network()
            result = await network.get_dkktList()
            return result
        except Exception as e:
            print(f"❌ Ошибка в _get_kkt_list_async: {e}")
            return None

    def get_kkt_list(self) -> List[str]:
        """
        Синхронная обертка для асинхронного метода
        Возвращает список серийных номеров касс
        """
        print("🔍 get_kkt_list() вызван")

        try:
            # Создаем или получаем event loop
            loop = self._get_or_create_event_loop()

            # Запускаем асинхронную операцию
            cash_info = loop.run_until_complete(self._get_kkt_list_async())

            if cash_info and cash_info.kkt:
                print(f"📦 Получены данные: {len(cash_info.kkt)} касс")

                # Кэшируем для последующего использования
                self._cached_result = cash_info

                # Извлекаем серийные номера
                kkt_serials = []
                for i, kkt in enumerate(cash_info.kkt, 1):
                    kkt_serials.append(kkt.kktSerial)
                    print(f"  {i}. Серийный номер: {kkt.kktSerial} - {kkt.modelName}")

                print(f"📊 Итоговый список серийных номеров: {kkt_serials}")
                return kkt_serials
            else:
                print("❌ Нет данных о кассах")
                return []

        except Exception as e:
            print(f"❌ Ошибка в get_kkt_list: {e}")
            return []

    def get_full_kkt_info(self) -> Optional[CashInfo]:
        """
        Синхронная обертка для получения полной информации
        """
        print("🔍 get_full_kkt_info() вызван")

        # Если есть кэшированные данные, возвращаем их
        if self._cached_result:
            print("📦 Возвращаем кэшированные данные")
            return self._cached_result

        # Иначе запрашиваем заново
        try:
            loop = self._get_or_create_event_loop()
            cash_info = loop.run_until_complete(self._get_kkt_list_async())
            self._cached_result = cash_info
            return cash_info
        except Exception as e:
            print(f"❌ Ошибка в get_full_kkt_info: {e}")
            return None

    async def close_async(self):
        """Асинхронное закрытие соединения"""
        if self._network:
            await self._network.close()
            self._network = None
            print("🔒 Сетевое соединение закрыто асинхронно")

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
                print(f"⚠️ Ошибка при закрытии: {e}")

        if self._loop and not self._loop.is_closed():
            self._loop.close()
            self._loop = None

        self._executor.shutdown(wait=False)

    def __del__(self):
        """Деструктор"""
        self.close()

class KKTController(QObject):
    """
    Контроллер для управления кассами
    """

    # Сигналы для обновления UI
    kktListChanged = Signal()
    selectedKktChanged = Signal()
    loadingChanged = Signal()
    kktInfoChanged = Signal()

    # Новые сигналы для передачи данных между потоками
    kktListUpdated = Signal(list)
    kktInfoUpdated = Signal(dict)

    def __init__(self, parent=None, use_test_data=True):  # ИЗМЕНЕНИЕ: добавить параметр
        super().__init__(parent)
        print(f"✅ KKTController инициализирован (test_data={use_test_data})")

        self._kkt_list = []
        self._selected_kkt = ""
        self._is_loading = False
        self._kkt_command = KKTCommand(use_test_data=use_test_data)  # ИЗМЕНЕНИЕ: передать флаг
        self._current_kkt_info = None

        # Подключаем сигналы
        self.kktListUpdated.connect(self._on_refresh_complete)
        self.kktInfoUpdated.connect(self._on_info_loaded)

        # Загружаем данные через 500 мс
        QTimer.singleShot(500, self.refresh_kkt_list)

    @Property(list, notify=kktListChanged)
    def kktList(self):
        return self._kkt_list

    @Property(str, notify=selectedKktChanged)
    def selectedKkt(self):
        return self._selected_kkt

    @Property(bool, notify=loadingChanged)
    def isLoading(self):
        return self._is_loading

    # Убираем QVariant, используем object
    @Property('QVariant', notify=kktInfoChanged)
    def kktInfo(self):
        return self._current_kkt_info

    @Slot()
    def refresh_kkt_list(self):
        """Обновляет список касс"""
        print("🔄 refresh_kkt_list вызван")

        self._is_loading = True
        self.loadingChanged.emit()

        # Запускаем в отдельном потоке
        from threading import Thread
        thread = Thread(target=self._refresh_kkt_list_thread)
        thread.daemon = True
        thread.start()

    def _refresh_kkt_list_thread(self):
        """Выполняется в отдельном потоке"""
        try:
            new_kkt_list = self._kkt_command.get_kkt_list()

            # Используем сигнал для передачи данных
            self.kktListUpdated.emit(new_kkt_list)

        except Exception as e:
            print(f"❌ Ошибка в потоке: {e}")
            self.kktListUpdated.emit([])

    @Slot(list)
    def _on_refresh_complete(self, kkt_list):
        """Слот для обновления UI после завершения потока"""
        self._kkt_list = kkt_list
        print(f"✅ Список обновлен: {len(kkt_list)} элементов")
        self.kktListChanged.emit()
        self._is_loading = False
        self.loadingChanged.emit()

    @Slot(str)
    def select_kkt(self, kkt_serial: str):
        """Выбирает кассу по серийному номеру"""
        print(f"🎯 select_kkt({kkt_serial})")

        if self._selected_kkt != kkt_serial:
            self._selected_kkt = kkt_serial
            self.selectedKktChanged.emit()

            # Загружаем информацию в отдельном потоке
            from threading import Thread
            thread = Thread(target=self._load_kkt_info_thread, args=(kkt_serial,))
            thread.daemon = True
            thread.start()





    def _load_kkt_info_thread(self, kkt_serial: str):
        """Загружает информацию о кассе в отдельном потоке"""
        print(f"🔍 Загрузка информации для кассы: {kkt_serial}")

        cash_info = self._kkt_command.get_full_kkt_info()

        if cash_info and cash_info.kkt:
            for kkt in cash_info.kkt:
                if kkt.kktSerial == kkt_serial:
                    info_dict = {
                        'kktSerial': kkt.kktSerial,
                        'fnSerial': kkt.fnSerial,
                        'kktInn': kkt.kktInn,
                        'kktRnm': kkt.kktRnm,
                        'modelName': kkt.modelName,
                        'dkktVersion': kkt.dkktVersion,
                        'developer': kkt.developer,
                        'manufacturer': kkt.manufacturer,
                        'shiftState': kkt.shiftState.value
                    }

                    # Используем сигнал для передачи данных
                    self.kktInfoUpdated.emit(info_dict)
                    return

        # Если касса не найдена
        self.kktInfoUpdated.emit(None)

    @Slot(dict)
    def _on_info_loaded(self, info_dict):
        """Слот для обновления информации о кассе"""
        self._current_kkt_info = info_dict
        self.kktInfoChanged.emit()
        if info_dict:
            print(f"✅ Информация загружена для кассы: {info_dict.get('kktSerial')}")
        else:
            print(f"⚠️ Информация не найдена")

    @Slot()
    def clear_selection(self):
        """Сбрасывает выбор"""
        print("🧹 clear_selection()")
        self._selected_kkt = ""
        self._current_kkt_info = None
        self.selectedKktChanged.emit()
        self.kktInfoChanged.emit()

    def close(self):
        """Закрывает соединение"""
        if self._kkt_command:
            self._kkt_command.close()

    def __del__(self):
        """Деструктор"""
        self.close()


class TSPIoTQmlLoader(QMainWindow):
    def __init__(self,
                 window_size: tuple,
                 app_icon_path: str,
                 header_name: str,
                 fonts_path: str,
                 qml_file: str,
                 use_test_data = True
                 ):
        super().__init__()

        # Создаем контроллер
        self._kkt_controller = KKTController(use_test_data=use_test_data)

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

    def __set_app_icon(self):
        if os.path.exists(self.app_icon_path):
            self.setWindowIcon(QIcon(self.app_icon_path))
            print(f"✅ Иконка загружена: {self.app_icon_path}")
        else:
            print(f"❌ Иконка не найдена: {self.app_icon_path}")

    def __load_fonts(self, fonts_dir):
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


def main():
    # Параметры
    SRC_DIR = os.path.dirname(os.path.abspath(__file__))
    __WINDOW_SIZE = (600, 700)
    __APP_HEADER_TITLE = "ТС ПИоТ - Тест касс"
    __APP_ICON_PATH = os.path.join(SRC_DIR, "ui", "assets", "image_89.png")
    __FONTS_PATH = os.path.join(SRC_DIR, "ui", "fonts")
    __QML_PATH = os.path.join(SRC_DIR, "ui", "simple.qml")

    app = QApplication(sys.argv)

    # Создаем и показываем окно
    loader = TSPIoTQmlLoader(
        window_size=__WINDOW_SIZE,
        app_icon_path=__APP_ICON_PATH,
        header_name=__APP_HEADER_TITLE,
        fonts_path=__FONTS_PATH,
        qml_file=__QML_PATH,
        use_test_data=True
    )

    loader.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()