from src.services.kkt_service import KKTService
from src.storage.application_storage import AppStorage

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


    # ТЕСТ 1: Первая загрузка
    def test1_first_load():
        print("\n" + "=" * 50)
        print("🚀 ТЕСТ 1: ПЕРВАЯ ЗАГРУЗКА ДАННЫХ")
        print("=" * 50)

        print_state()
        print("\n   ▶️ Запускаем start_loading()...")
        storage.load_kkt()

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
        storage.load_kkt()

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
        storage.reload_kkt()

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
            storage.set_current_cash(first_serial)

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
            storage.reload_kkt()

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
        print(f"      - Максимум потоков: {storage._executor._threadpool.maxThreadCount()}")
        print(f"      - Активных потоков: {storage._executor._threadpool.activeThreadCount()}")
        print(f"   📊 Статистика сигналов:")
        print(f"      - list_changed: {callbacks_count['list_changed']}")
        print(f"      - current_changed: {callbacks_count['current_changed']}")
        print(f"      - loading_changed: {callbacks_count['loading_changed']}")
        print(f"      - errors: {callbacks_count['error']}")




    # ТЕСТ 8: Истечение кэша
    def test8_cache_expiry():
        print("\n" + "=" * 50)
        print("🚀 ТЕСТ 8: ИСТЕЧЕНИЕ КЭША")
        print("=" * 50)

        print(f"\n 📅 Кэш истекает через {storage._cache._cache_ttl} секунд")
        print(f"   📅 Последнее обновление: {storage._cache._last_update}")
        print(f"   ✅ Кэш валиден сейчас: {storage._cache._is_cache_valid()}")

        print(f"\n   ⏳ Ждём {storage._cache._cache_ttl + 1} секунд до истечения кэша...")
        QTimer.singleShot((storage._cache._cache_ttl + 1) * 1000, test8_check)


    def test8_check():
        print(f"\n   📅 Кэш валиден после ожидания: {storage._cache._is_cache_valid()}")

        if not storage._cache._is_cache_valid():
            print("\n   ✅ Кэш успешно истёк!")

            # Пробуем загрузить снова (должна быть реальная загрузка)
            print("\n   ▶️ Пробуем загрузить данные после истечения кэша...")
            storage.reload_kkt()
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