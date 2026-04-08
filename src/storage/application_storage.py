# storage/app_storage.py
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from PySide6.QtCore import QObject, Signal, QThreadPool, QMutex, QMutexLocker
from src.dto.kkt import CashInfo, KktInfo
from src.services.kkt_service import KKTService
from src.workers.kkt_worker import KKTWorker


class AppStorage(QObject):
    """Хранилище состояния с асинхронной загрузкой через воркеров"""

    kktListChanged = Signal()
    currentSerialChanged = Signal()
    loadingChanged = Signal()
    errorChanged = Signal()

    def __init__(self, kkt_service: KKTService, cache_ttl_seconds: int = 300, parent=None):
        super().__init__(parent)
        self._service = kkt_service
        self._cache_ttl = cache_ttl_seconds

        # Thread pool для выполнения воркеров
        self._threadpool = QThreadPool()
        self._threadpool.setMaxThreadCount(3)

        # Данные
        self._kkt_list: list = []
        self._kkt_info_cache: Dict[str, dict] = {}
        self._current_serial: str = ""
        self._is_loading: bool = False
        self._error: str = ""
        self._last_update: Optional[datetime] = None

        # Активные воркеры
        self._active_workers = 0
        self._mutex = QMutex()

    # ─── Public Methods ─────────────────────────────────────────

    def start_loading(self, force: bool = False):
        """Асинхронно загружает список касс"""
        if self._is_loading:
            return

        if not force and self._is_cache_valid() and self._kkt_list:
            return

        self._set_loading(True)
        self._set_error("")

        # ✅ Создаём воркер с МЕТОДОМ сервиса
        worker = KKTWorker(self._service.get_kkt_list)
        worker.signals.finished.connect(self._on_loading_finished)
        worker.signals.error.connect(self._on_loading_error)

        self._active_workers += 1
        self._threadpool.start(worker)  # ← ЗАПУСКАЕМ воркер!

    def refresh_kkt_info(self, serial: str):
        """Обновить информацию о конкретной кассе"""
        if self._is_loading:
            return

        self._set_loading(True)

        # ✅ Передаём метод сервиса с аргументом
        worker = KKTWorker(self._service.get_kkt_by_serial, serial)
        worker.signals.finished.connect(
            lambda result: self._on_refresh_finished(serial, result)
        )
        worker.signals.error.connect(self._on_loading_error)

        self._active_workers += 1
        self._threadpool.start(worker)  # ← ЗАПУСКАЕМ воркер!

    def get_open_shifts_async(self):
        """Асинхронно получить кассы с открытыми сменами"""
        if self._is_loading:
            return

        self._set_loading(True)

        # ✅ Любой метод сервиса можно запустить в воркере
        worker = KKTWorker(self._service.get_open_shifts)
        worker.signals.finished.connect(self._on_open_shifts_loaded)
        worker.signals.error.connect(self._on_loading_error)

        self._active_workers += 1
        self._threadpool.start(worker)

    def get_kkt_info(self, serial: str) -> dict:
        """Возвращает информацию о кассе из кэша"""
        with QMutexLocker(self._mutex):
            return self._kkt_info_cache.get(serial, {})

    def set_current(self, serial: str):
        """Устанавливает текущую кассу"""
        if self._current_serial != serial and serial in self._kkt_info_cache:
            self._current_serial = serial
            self.currentSerialChanged.emit()

    @property
    def kktList(self) -> list:
        return self._kkt_list

    @property
    def currentSerial(self) -> str:
        return self._current_serial

    @property
    def is_loading(self) -> bool:
        return self._is_loading

    @property
    def error(self) -> str:
        return self._error

    # ─── Private Methods ────────────────────────────────────────

    def _is_cache_valid(self) -> bool:
        if self._last_update is None:
            return False
        return datetime.now() - self._last_update < timedelta(seconds=self._cache_ttl)

    def _set_loading(self, loading: bool):
        self._is_loading = loading
        self.loadingChanged.emit()

    def _set_error(self, error: str):
        self._error = error
        self.errorChanged.emit()

    def _on_loading_finished(self, result: Optional[CashInfo]):
        """Обработчик результата загрузки"""
        self._active_workers -= 1

        if result is None:
            self._set_error("Не удалось загрузить список касс")
        else:
            with QMutexLocker(self._mutex):
                self._update_cache(result)
                self._last_update = datetime.now()

                if not self._current_serial and self._kkt_list:
                    self._current_serial = self._kkt_list[0].get('kktSerial', '')
                    self.currentSerialChanged.emit()

                self.kktListChanged.emit()

        if self._active_workers == 0:
            self._set_loading(False)

    def _on_refresh_finished(self, serial: str, result: Optional[KktInfo]):
        """Обработчик обновления конкретной кассы"""
        self._active_workers -= 1

        if result:
            with QMutexLocker(self._mutex):
                kkt_dict = self._kkt_to_dict(result)
                self._kkt_info_cache[serial] = kkt_dict

                # Обновляем список
                for i, item in enumerate(self._kkt_list):
                    if item.get('kktSerial') == serial:
                        self._kkt_list[i] = kkt_dict
                        break

                self.kktListChanged.emit()

                if self._current_serial == serial:
                    self.currentSerialChanged.emit()

        if self._active_workers == 0:
            self._set_loading(False)

    def _on_open_shifts_loaded(self, result: List[KktInfo]):
        """Обработчик загрузки касс с открытыми сменами"""
        self._active_workers -= 1
        # Можно сделать что-то с результатом
        print(f"Найдено касс с открытой сменой: {len(result)}")

        if self._active_workers == 0:
            self._set_loading(False)

    def _on_loading_error(self, error_msg: str):
        self._active_workers -= 1
        self._set_error(error_msg)

        if self._active_workers == 0:
            self._set_loading(False)

    def _update_cache(self, cash_info: CashInfo):
        """Обновляет кэш из DTO"""
        self._kkt_list.clear()
        self._kkt_info_cache.clear()

        for kkt in cash_info.kkt:
            kkt_dict = self._kkt_to_dict(kkt)
            self._kkt_list.append(kkt_dict)
            self._kkt_info_cache[kkt.kktSerial] = kkt_dict

    def _kkt_to_dict(self, kkt: KktInfo) -> dict:
        return {
            'kktSerial': kkt.kktSerial,
            'fnSerial': kkt.fnSerial,
            'kktInn': kkt.kktInn,
            'kktRnm': kkt.kktRnm,
            'modelName': kkt.modelName,
            'dkktVersion': kkt.dkktVersion,
            'developer': kkt.developer,
            'manufacturer': kkt.manufacturer,
            'shiftState': kkt.shiftState.value,
            'displayName': f"{kkt.kktRnm} ({kkt.kktSerial})",
            'isShiftOpen': kkt.shiftState.value == "Открыта"
        }


# storage/app_storage.py

# ... (весь ваш существующий код с KKTService) ...


# ============================================================================
# ТЕСТОВЫЙ БЛОК ДЛЯ ПРОВЕРКИ РАБОТЫ ПОТОКОВ
# ============================================================================

if __name__ == "__main__":
    import sys
    import time
    from PySide6.QtCore import QCoreApplication, QTimer
    from threading import current_thread
    from src.workers.kkt_worker import KKTWorker  # Импортируем воркер

    print("\n" + "=" * 70)
    print("🧪 ТЕСТИРОВАНИЕ APPSTORAGE С ПОТОКАМИ")
    print("=" * 70)

    # Создаём Qt приложение без GUI
    app = QCoreApplication(sys.argv)

    # Создаём зависимости
    print("\n📦 1. СОЗДАНИЕ ЗАВИСИМОСТЕЙ")
    print("-" * 50)

    print("   Создаём KKTService...")
    service = KKTService()

    print("   Создаём AppStorage (TTL=10 сек)...")
    storage = AppStorage(service, cache_ttl_seconds=10)

    # Счётчик для отслеживания
    callbacks_count = {
        'list_changed': 0,
        'current_changed': 0,
        'loading_changed': 0,
        'error': 0
    }


    # Функции-обработчики сигналов
    def on_list_changed():
        callbacks_count['list_changed'] += 1
        print(f"  📢 [Поток: {current_thread().name}] Сигнал: Список касс обновлен (всего: {len(storage.kktList)})")


    def on_current_changed():
        callbacks_count['current_changed'] += 1
        print(f"  📢 [Поток: {current_thread().name}] Сигнал: Текущая касса -> {storage.currentSerial}")


    def on_loading_changed():
        callbacks_count['loading_changed'] += 1
        status = "🚀 НАЧАЛСЯ" if storage.is_loading else "✅ ЗАКОНЧИЛСЯ"
        print(f"  📢 [Поток: {current_thread().name}] Сигнал: Процесс загрузки {status}")


    def on_error_changed():
        if storage.error:
            callbacks_count['error'] += 1
            print(f"  ❌ [Поток: {current_thread().name}] Сигнал: Ошибка - {storage.error}")


    # Подключаем сигналы
    print("\n🔌 2. ПОДКЛЮЧЕНИЕ СИГНАЛОВ")
    print("-" * 50)

    storage.kktListChanged.connect(on_list_changed)
    storage.currentSerialChanged.connect(on_current_changed)
    storage.loadingChanged.connect(on_loading_changed)
    storage.errorChanged.connect(on_error_changed)

    print("   ✅ Сигналы подключены")


    # Функция для вывода текущего состояния
    def print_state():
        print(f"\n📊 ТЕКУЩЕЕ СОСТОЯНИЕ (Поток: {current_thread().name}):")
        print(f"   - Загрузка: {storage.is_loading}")
        print(f"   - Ошибка: {storage.error if storage.error else 'нет'}")
        print(f"   - Касс в кэше: {len(storage.kktList)}")
        print(f"   - Текущая касса: {storage.currentSerial if storage.currentSerial else 'не выбрана'}")
        print(f"   - Активных воркеров: {storage._active_workers}")


    # ТЕСТ 1: Первая загрузка
    def test1_first_load():
        print("\n" + "=" * 50)
        print("🚀 ТЕСТ 1: ПЕРВАЯ ЗАГРУЗКА ДАННЫХ")
        print("=" * 50)

        print_state()
        print("\n   ▶️ Запускаем start_loading()...")
        storage.start_loading()

        # Ждём 2 секунды для частичной загрузки
        QTimer.singleShot(2000, lambda: test1_check())


    def test1_check():
        print_state()

        if len(storage.kktList) > 0:
            print(f"\n   ✅ Успешно загружено {len(storage.kktList)} касс!")
            print(f"\n   📋 Первые 3 кассы:")
            for i, kkt in enumerate(storage.kktList[:3], 1):
                print(f"      {i}. {kkt.get('displayName')} - {kkt.get('shiftState')}")

            # Переходим к следующему тесту
            test2_second_load()
        else:
            print("\n   ⚠️ Данные ещё не загружены, ждём ещё 2 секунды...")
            QTimer.singleShot(2000, test1_check)


    # ТЕСТ 2: Повторная загрузка (должна использовать кэш)
    def test2_second_load():
        print("\n" + "=" * 50)
        print("🚀 ТЕСТ 2: ПОВТОРНАЯ ЗАГРУЗКА (ДОЛЖНА ИСПОЛЬЗОВАТЬ КЭШ)")
        print("=" * 50)

        print_state()
        print("\n   ▶️ Запускаем start_loading() повторно...")
        old_list_id = id(storage.kktList)
        storage.start_loading()

        # Проверяем, что загрузка не началась (кэш валиден)
        QTimer.singleShot(500, lambda: test2_check(old_list_id))


    def test2_check(old_list_id):
        print_state()

        if id(storage.kktList) == old_list_id:
            print("\n   ✅ Кэш работает! Повторная загрузка не произошла.")
        else:
            print("\n   ⚠️ Внимание! Кэш не сработал, данные перезагружены.")

        test3_force_load()


    # ТЕСТ 3: Принудительная загрузка
    def test3_force_load():
        print("\n" + "=" * 50)
        print("🚀 ТЕСТ 3: ПРИНУДИТЕЛЬНАЯ ЗАГРУЗКА (force=True)")
        print("=" * 50)

        print_state()
        print("\n   ▶️ Запускаем start_loading(force=True)...")
        storage.start_loading(force=True)

        # Ждём завершения
        QTimer.singleShot(3000, test3_check)


    def test3_check():
        print_state()
        print("\n   ✅ Принудительная загрузка выполнена!")

        test4_select_kkt()


    # ТЕСТ 4: Выбор кассы
    def test4_select_kkt():
        print("\n" + "=" * 50)
        print("🚀 ТЕСТ 4: ВЫБОР КАССЫ")
        print("=" * 50)

        if storage.kktList:
            first_serial = storage.kktList[0].get('kktSerial')
            print(f"   📋 Доступные кассы: {[k.get('kktSerial') for k in storage.kktList[:3]]}")
            print(f"\n   ▶️ Выбираем кассу: {first_serial}")
            storage.set_current(first_serial)

            # Получаем информацию о выбранной кассе
            info = storage.get_kkt_info(first_serial)
            print(f"\n   📄 Информация о выбранной кассе:")
            print(f"      - Название: {info.get('kktRnm', 'N/A')}")
            print(f"      - Серийник: {info.get('kktSerial', 'N/A')}")
            print(f"      - Состояние смены: {info.get('shiftState', 'N/A')}")
            print(f"      - Смена открыта: {info.get('isShiftOpen', False)}")
            print(f"      - ИНН: {info.get('kktInn', 'N/A')}")
            print(f"      - Модель: {info.get('modelName', 'N/A')}")
        else:
            print("   ⚠️ Нет загруженных касс для выбора")

        test5_refresh_kkt()


    # ТЕСТ 5: Обновление конкретной кассы
    def test5_refresh_kkt():
        print("\n" + "=" * 50)
        print("🚀 ТЕСТ 5: ОБНОВЛЕНИЕ КОНКРЕТНОЙ КАССЫ")
        print("=" * 50)

        if storage.kktList:
            first_serial = storage.kktList[0].get('kktSerial')
            print(f"   ▶️ Обновляем кассу: {first_serial}")
            storage.refresh_kkt_info(first_serial)

            # Ждём обновления
            QTimer.singleShot(3000, test5_check)
        else:
            print("   ⚠️ Нет загруженных касс для обновления")
            test6_thread_info()


    def test5_check():
        print_state()
        print("   ✅ Обновление кассы выполнено!")
        test6_thread_info()


    # ТЕСТ 6: Информация о потоках
    def test6_thread_info():
        print("\n" + "=" * 50)
        print("🚀 ТЕСТ 6: ИНФОРМАЦИЯ О ПОТОКАХ")
        print("=" * 50)

        print(f"\n   🧵 Главный поток: {current_thread().name}")
        print(f"   🏊‍♂️ QThreadPool:")
        print(f"      - Максимум потоков: {storage._threadpool.maxThreadCount()}")
        print(f"      - Активных потоков: {storage._threadpool.activeThreadCount()}")
        print(f"   📊 Статистика сигналов:")
        print(f"      - list_changed: {callbacks_count['list_changed']}")
        print(f"      - current_changed: {callbacks_count['current_changed']}")
        print(f"      - loading_changed: {callbacks_count['loading_changed']}")
        print(f"      - errors: {callbacks_count['error']}")

        test7_worker_creation()


    # ТЕСТ 7: Создание и запуск воркера напрямую
    def test7_worker_creation():
        print("\n" + "=" * 50)
        print("🚀 ТЕСТ 7: ПРЯМОЙ ЗАПУСК ВОРКЕРА")
        print("=" * 50)

        print("\n   ▶️ Создаём воркер напрямую...")

        # Создаём воркер для теста
        def test_function():
            """Тестовая функция, которая выполнится в потоке"""
            import time
            print(f"   🔧 [Поток: {current_thread().name}] Выполняю тестовую функцию...")
            time.sleep(1)
            return "Тестовый результат"

        worker = KKTWorker(test_function)
        worker.signals.finished.connect(lambda result: test7_callback(result))
        worker.signals.error.connect(lambda error: print(f"   ❌ Ошибка в воркере: {error}"))

        print("   ▶️ Запускаем воркер...")
        storage._threadpool.start(worker)

        # Ждём результат
        QTimer.singleShot(2000, test7_wait)


    def test7_callback(result):
        print(f"   ✅ [Поток: {current_thread().name}] Воркер завершился с результатом: {result}")


    def test7_wait():
        print("\n   ✅ Воркер успешно выполнен!")

        test8_cache_expiry()


    # ТЕСТ 8: Истечение кэша
    def test8_cache_expiry():
        print("\n" + "=" * 50)
        print("🚀 ТЕСТ 8: ИСТЕЧЕНИЕ КЭША")
        print("=" * 50)

        print(f"\n   📅 Кэш истекает через {storage._cache_ttl} секунд")
        print(f"   📅 Последнее обновление: {storage._last_update}")
        print(f"   ✅ Кэш валиден сейчас: {storage._is_cache_valid()}")

        print(f"\n   ⏳ Ждём {storage._cache_ttl + 1} секунд до истечения кэша...")
        QTimer.singleShot((storage._cache_ttl + 1) * 1000, test8_check)


    def test8_check():
        print(f"\n   📅 Кэш валиден после ожидания: {storage._is_cache_valid()}")

        if not storage._is_cache_valid():
            print("\n   ✅ Кэш успешно истёк!")

            # Пробуем загрузить снова (должна быть реальная загрузка)
            print("\n   ▶️ Пробуем загрузить данные после истечения кэша...")
            storage.start_loading()

            QTimer.singleShot(3000, finish_test)
        else:
            print("\n   ⚠️ Кэш не истёк! Возможно, проблема с таймингом.")
            finish_test()


    # Завершение тестов
    def finish_test():
        print("\n" + "=" * 70)
        print("✅ ВСЕ ТЕСТЫ ЗАВЕРШЕНЫ")
        print("=" * 70)

        print(f"\n📊 ИТОГОВАЯ СТАТИСТИКА:")
        print(f"   - Загружено касс: {len(storage.kktList)}")
        print(f"   - Текущая касса: {storage.currentSerial}")
        print(f"   - Ошибок: {storage.error if storage.error else 'нет'}")
        print(f"   - Сигналов получено: {sum(callbacks_count.values())}")

        print(f"\n🔍 ДЕТАЛИЗАЦИЯ ПО КАССАМ:")
        for i, kkt in enumerate(storage.kktList[:5], 1):
            print(f"   {i}. {kkt.get('kktRnm')} - {kkt.get('shiftState')}")

        if len(storage.kktList) > 5:
            print(f"   ... и ещё {len(storage.kktList) - 5} касс")

        print("\n⏹️ Завершаем работу...")
        app.quit()


    # Запускаем первый тест
    print("\n🎬 НАЧАЛО ТЕСТИРОВАНИЯ")
    print("=" * 70)
    test1_first_load()

    # Запускаем event loop
    sys.exit(app.exec())