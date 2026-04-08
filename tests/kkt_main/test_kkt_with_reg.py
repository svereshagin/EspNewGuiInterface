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

from old_src.domain.kkt.entity import CashInfo, ShiftState, KktInfo
from new_src.network.kkt import KKTNetwork
from old_src.network.controlmodule import ControlmoduleNetwork
from old_src.network.tspiot import TspiotSetup, RequestCreateInstanceTSPIOT_DTO, RequestRegistrationTSPIOT_DTO

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('tspiot_debug.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class TSPIOTCommand:
    """Класс для работы с TSPIOT - регистрация и создание экземпляров"""

    def __init__(self, use_test_data=False):
        self._network = None
        self._tspiot_setup = TspiotSetup()
        self._controlmodule_network = ControlmoduleNetwork()
        self._loop = None
        self._executor = ThreadPoolExecutor(max_workers=1)
        self._use_test_data = use_test_data
        logger.info("🔧 TSPIOTCommand инициализирован (test_data=%s)", use_test_data)

    def _get_or_create_event_loop(self):
        """Получает или создает event loop"""
        try:
            self._loop = asyncio.get_running_loop()
        except RuntimeError:
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
        return self._loop

    def get_cm_instances(self) -> List[str]:
        """
        Получает список ID зарегистрированных экземпляров ТС ПИоТ
        БЕЗ КЭШИРОВАНИЯ - всегда запрашивает актуальные данные
        """
        logger.debug("🔍 get_cm_instances() вызван - запрос актуальных данных")

        #TODO в будущем здесь улучшить план создания
        # if self._use_test_data:
        #     logger.info("🧪 Используем тестовые данные")
        #     return ["00106327428745"]  # Одна зарегистрированная касса

        try:
            # Реальный запрос к API
            logger.debug("📡 Выполняем запрос к API для получения экземпляров")
            instances_dto = self._controlmodule_network._get_cm_instances()
            logger.info(f"📦 Получен объект instances_dto: {instances_dto}")
            if instances_dto and hasattr(instances_dto, 'instances'):
                logger.info(
                    f"📋 Количество экземпляров: {len(instances_dto.instances) if instances_dto.instances else 0}")
                for i, inst in enumerate(instances_dto.instances or []):
                    logger.info(f"  {i + 1}. ID: {inst.id}, Статус: {inst.serviceState}")
            else:
                logger.warning("⚠️ instances_dto пуст или не имеет атрибута instances")
            if instances_dto and instances_dto.instances:
                # Извлекаем ID всех экземпляров
                registered_ids = [inst.id for inst in instances_dto.instances]
                logger.info(f"📋 Получены зарегистрированные ID из API: {registered_ids}")

                # Детальное логирование каждого экземпляра
                for inst in instances_dto.instances:
                    logger.debug(f"  • ID: {inst.id}, Статус: {inst.serviceState}, Порт: {inst.port}, "
                                 f"Время создания: {getattr(inst, 'createdAt', 'N/A')}")

                return registered_ids
            else:
                logger.info("ℹ️ Нет зарегистрированных экземпляров (пустой ответ от API)")
                return []

        except AttributeError as e:
            logger.error(f"❌ Ошибка атрибута при получении экземпляров: {e}", exc_info=True)
            return []
        except Exception as e:
            logger.error(f"❌ Ошибка получения экземпляров: {e}", exc_info=True)
            return []

    def is_kkt_registered(self, kkt_serial: str) -> bool:
        """
        Проверяет, зарегистрирована ли касса по серийному номеру
        Всегда запрашивает актуальные данные
        """
        logger.debug(f"🔍 Проверка регистрации кассы: {kkt_serial}")
        instances = self.get_cm_instances()
        print(instances)
        is_registered = instances and kkt_serial in instances
        logger.info(f"📊 Касса {kkt_serial} зарегистрирована: {is_registered}")
        return is_registered

    def create_esm_service(self, kkt_serial: str, port: int = None, soft_port: int = None) -> dict:
        """
        Создает экземпляр ESM сервиса
        """
        logger.info(f"🔧 create_esm_service для {kkt_serial} (port={port}, soft_port={soft_port})")

        if self._use_test_data:
            logger.info("🧪 Имитация создания ESM сервиса (тестовый режим)")
            return {
                'success': True,
                'tspiot_id': f"tspiot_{kkt_serial}",
                'status': "Работает",
                'error_message': None
            }

        try:
            data = RequestCreateInstanceTSPIOT_DTO(
                kkt_serial=kkt_serial,
                port=port,
                softPort=soft_port
            )
            logger.debug(f"📤 Отправка запроса на создание ESM: {data}")
            result = self._tspiot_setup.create_esm_service(data)
            logger.info(f"📥 Ответ от create_esm_service: {result}")

            return {
                'success': result.success,
                'tspiot_id': result.tspiot_id,
                'status': result.status,
                'error_message': result.error_message
            }
        except Exception as e:
            logger.error(f"❌ Ошибка создания ESM: {e}", exc_info=True)
            return {
                'success': False,
                'error_message': str(e)
            }

    def register_tspiot(self, instance_id: str, kkt_serial: str, fn_serial: str, kkt_inn: str) -> dict:
        """
        Регистрирует TSPIOT
        """
        logger.info(f"🔧 register_tspiot для {kkt_serial} (instance_id={instance_id})")
        logger.debug(f"  ФН: {fn_serial}, ИНН: {kkt_inn}")

        if self._use_test_data:
            logger.info("🧪 Имитация регистрации TSPIOT (тестовый режим)")
            return {
                'success': True,
                'tspiot_id': f"reg_{kkt_serial}"
            }

        try:
            data = RequestRegistrationTSPIOT_DTO(
                id=instance_id,
                kktSerial=kkt_serial,
                fnSerial=fn_serial,
                kktInn=kkt_inn
            )
            logger.debug(f"📤 Отправка запроса на регистрацию: {data}")
            result = self._tspiot_setup.register_tspiot(data)
            logger.info(f"📥 Ответ от register_tspiot: {result}")

            if isinstance(result, dict) and 'success' in result:
                return result
            elif hasattr(result, 'tspiotId'):
                return {
                    'success': True,
                    'tspiot_id': result.tspiotId
                }
            else:
                logger.warning(f"⚠️ Неизвестный формат ответа: {result}")
                return {
                    'success': False,
                    'error_message': "Неизвестный ответ от сервера"
                }
        except Exception as e:
            logger.error(f"❌ Ошибка регистрации: {e}", exc_info=True)
            return {
                'success': False,
                'error_message': str(e)
            }

    def close(self):
        """Закрывает соединения"""
        logger.info("🔒 Закрытие TSPIOTCommand")
        if self._controlmodule_network:
            self._controlmodule_network.close()
        if self._loop and not self._loop.is_closed():
            self._loop.close()
            self._loop = None
        self._executor.shutdown(wait=False)

    def __del__(self):
        self.close()


class KKTCommand:
    """Класс для работы с сетью - возвращает данные от API"""

    def __init__(self, use_test_data=True):
        self._cached_result = None
        self._network = None
        self._loop = None
        self._executor = ThreadPoolExecutor(max_workers=1)
        self._use_test_data = use_test_data
        logger.info(f"🔧 KKTCommand инициализирован (test_data={use_test_data})")

    def _get_test_data(self) -> CashInfo:
        """Возвращает тестовые данные"""
        logger.info("🧪 Используем тестовые данные")
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
        """Получает или создает экземпляр KKTNetwork"""
        if self._use_test_data:
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
        if self._use_test_data:
            return self._get_test_data()
        try:
            network = self._get_network()
            result = await network.get_dkktList()
            return result
        except Exception as e:
            logger.error(f"❌ Ошибка в _get_kkt_list_async: {e}", exc_info=True)
            return None

    def get_kkt_list(self) -> List[str]:
        """
        Синхронная обертка для асинхронного метода
        Возвращает список серийных номеров касс
        """
        logger.info("🔍 get_kkt_list() вызван")

        try:
            loop = self._get_or_create_event_loop()
            cash_info = loop.run_until_complete(self._get_kkt_list_async())

            if cash_info and cash_info.kkt:
                logger.info(f"📦 Получены данные: {len(cash_info.kkt)} касс")
                self._cached_result = cash_info

                kkt_serials = []
                for i, kkt in enumerate(cash_info.kkt, 1):
                    kkt_serials.append(kkt.kktSerial)
                    logger.info(f"  {i}. Серийный номер: {kkt.kktSerial} - {kkt.modelName}")

                logger.info(f"📊 Итоговый список серийных номеров: {kkt_serials}")
                return kkt_serials
            else:
                logger.warning("❌ Нет данных о кассах")
                return []

        except Exception as e:
            logger.error(f"❌ Ошибка в get_kkt_list: {e}", exc_info=True)
            return []

    def get_full_kkt_info(self) -> Optional[CashInfo]:
        """
        Синхронная обертка для получения полной информации
        """
        logger.info("🔍 get_full_kkt_info() вызван")

        if self._cached_result:
            logger.info("📦 Возвращаем кэшированные данные")
            return self._cached_result

        try:
            loop = self._get_or_create_event_loop()
            cash_info = loop.run_until_complete(self._get_kkt_list_async())
            self._cached_result = cash_info
            return cash_info
        except Exception as e:
            logger.error(f"❌ Ошибка в get_full_kkt_info: {e}", exc_info=True)
            return None

    async def close_async(self):
        """Асинхронное закрытие соединения"""
        if self._network:
            await self._network.close()
            self._network = None
            logger.info("🔒 Сетевое соединение закрыто асинхронно")

    def close(self):
        """Синхронное закрытие соединения"""
        logger.info("🔒 Закрытие KKTCommand")
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


class KKTController(QObject):
    """
    Контроллер для управления кассами
    """

    # Сигналы
    kktListChanged = Signal()
    selectedKktChanged = Signal()
    loadingChanged = Signal()
    kktInfoChanged = Signal()
    registrationStatusChanged = Signal()
    registrationResultChanged = Signal(dict)
    kktListUpdated = Signal(list)
    kktInfoUpdated = Signal(dict)

    def __init__(self, parent=None, use_test_data=True):
        super().__init__(parent)
        logger.info(f"✅ KKTController инициализирован (test_data={use_test_data})")

        self._kkt_list = []
        self._selected_kkt = ""
        self._is_loading = False
        self._kkt_command = KKTCommand(use_test_data=use_test_data)
        self._tspiot_command = TSPIOTCommand(use_test_data=use_test_data)
        self._current_kkt_info = None

        # Подключаем сигналы
        self.kktListUpdated.connect(self._on_refresh_complete)
        self.kktInfoUpdated.connect(self._on_info_loaded)

        # Загружаем данные
        QTimer.singleShot(500, self.refresh_kkt_list)

    # Существующие свойства
    @Property(list, notify=kktListChanged)
    def kktList(self):
        return self._kkt_list

    @Property(str, notify=selectedKktChanged)
    def selectedKkt(self):
        return self._selected_kkt

    @Property(bool, notify=loadingChanged)
    def isLoading(self):
        return self._is_loading

    @Property('QVariant', notify=kktInfoChanged)
    def kktInfo(self):
        return self._current_kkt_info

    # Новое свойство - можно ли регистрировать (всегда актуальное)
    @Property(bool, notify=registrationStatusChanged)
    def canRegister(self):
        """Можно ли регистрировать выбранную кассу (всегда актуальная проверка)"""
        if not self._selected_kkt or not self._current_kkt_info:
            logger.debug(f"❌ Нельзя регистрировать: нет выбранной кассы или информации")
            return False

        # Всегда запрашиваем актуальный статус
        is_registered = self._tspiot_command.is_kkt_registered(self._selected_kkt)
        can_register = not is_registered

        logger.debug(f"📊 Статус регистрации для {self._selected_kkt}: "
                     f"зарегистрирована={is_registered}, можно регистрировать={can_register}")
        return can_register

    # Существующие слоты
    @Slot()
    def refresh_kkt_list(self):
        """Обновляет список касс"""
        logger.info("🔄 refresh_kkt_list вызван")

        self._is_loading = True
        self.loadingChanged.emit()

        from threading import Thread
        thread = Thread(target=self._refresh_kkt_list_thread)
        thread.daemon = True
        thread.start()

    def _refresh_kkt_list_thread(self):
        """Выполняется в отдельном потоке"""
        try:
            logger.debug("Запуск потока обновления списка касс")
            new_kkt_list = self._kkt_command.get_kkt_list()
            logger.info(f"Получен новый список касс: {new_kkt_list}")
            self.kktListUpdated.emit(new_kkt_list)
        except Exception as e:
            logger.error(f"❌ Ошибка в потоке обновления: {e}", exc_info=True)
            self.kktListUpdated.emit([])

    @Slot(list)
    def _on_refresh_complete(self, kkt_list):
        """Слот для обновления UI после завершения потока"""
        self._kkt_list = kkt_list
        logger.info(f"✅ Список обновлен: {len(kkt_list)} элементов")
        self.kktListChanged.emit()
        self._is_loading = False
        self.loadingChanged.emit()

        # Обновляем статус регистрации для выбранной кассы (если есть)
        if self._selected_kkt:
            self.registrationStatusChanged.emit()

    @Slot(str)
    def select_kkt(self, kkt_serial: str):
        """Выбирает кассу по серийному номеру"""
        logger.info(f"🎯 select_kkt({kkt_serial})")

        if self._selected_kkt != kkt_serial:
            self._selected_kkt = kkt_serial
            self.selectedKktChanged.emit()

            # Сразу проверяем статус регистрации
            is_registered = self._tspiot_command.is_kkt_registered(kkt_serial)
            logger.info(f"📊 Статус регистрации для {kkt_serial}: {is_registered}")
            self.registrationStatusChanged.emit()

            from threading import Thread
            thread = Thread(target=self._load_kkt_info_thread, args=(kkt_serial,))
            thread.daemon = True
            thread.start()

    def _load_kkt_info_thread(self, kkt_serial: str):
        """Загружает информацию о кассе в отдельном потоке"""
        logger.info(f"🔍 Загрузка информации для кассы: {kkt_serial}")

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
                        'shiftState': kkt.shiftState.value if hasattr(kkt.shiftState, 'value') else str(kkt.shiftState)
                    }
                    logger.info(f"✅ Информация загружена для {kkt_serial}")
                    self.kktInfoUpdated.emit(info_dict)
                    return

        logger.warning(f"⚠️ Информация не найдена для {kkt_serial}")
        self.kktInfoUpdated.emit(None)

    @Slot(dict)
    def _on_info_loaded(self, info_dict):
        """Слот для обновления информации о кассе"""
        self._current_kkt_info = info_dict
        self.kktInfoChanged.emit()

        # Проверяем статус регистрации для новой информации
        if info_dict and self._selected_kkt:
            is_registered = self._tspiot_command.is_kkt_registered(self._selected_kkt)
            logger.info(f"📊 После загрузки инфо - статус регистрации {self._selected_kkt}: {is_registered}")
            self.registrationStatusChanged.emit()

        if info_dict:
            logger.info(f"✅ Информация обновлена для кассы: {info_dict.get('kktSerial')}")
        else:
            logger.warning(f"⚠️ Информация не найдена")

    @Slot()
    def register_current_kkt(self):
        """Регистрирует выбранную кассу"""
        if not self._selected_kkt or not self._current_kkt_info:
            logger.error("❌ Нет выбранной кассы для регистрации")
            return

        logger.info(f"📝 Начало регистрации кассы: {self._selected_kkt}")
        logger.debug(f"Данные кассы: {self._current_kkt_info}")

        self._is_loading = True
        self.loadingChanged.emit()

        from threading import Thread
        thread = Thread(target=self._register_thread)
        thread.daemon = True
        thread.start()

    def _register_thread(self):
        """Процесс регистрации в отдельном потоке"""
        try:
            # Шаг 1: Создаем ESM сервис
            logger.info("📌 Шаг 1: Создание ESM сервиса")
            create_result = self._tspiot_command.create_esm_service(
                kkt_serial=self._selected_kkt
            )
            logger.info(f"Результат создания ESM: {create_result}")

            if not create_result.get('success'):
                error_msg = f"Ошибка создания ESM: {create_result.get('error_message')}"
                logger.error(f"❌ {error_msg}")
                self.registrationResultChanged.emit({
                    'success': False,
                    'step': 1,
                    'message': error_msg
                })
                return

            tspiot_id = create_result.get('tspiot_id')
            logger.info(f"✅ ESM сервис создан: {tspiot_id}")

            # Шаг 2: Регистрируем TSPIOT
            logger.info("📌 Шаг 2: Регистрация TSPIOT")
            register_result = self._tspiot_command.register_tspiot(
                instance_id=tspiot_id,
                kkt_serial=self._current_kkt_info['kktSerial'],
                fn_serial=self._current_kkt_info['fnSerial'],
                kkt_inn=self._current_kkt_info['kktInn']
            )
            logger.info(f"Результат регистрации: {register_result}")

            # Проверяем статус после регистрации (без кэширования)
            logger.info("📊 Проверка статуса после регистрации...")
            is_registered_now = self._tspiot_command.is_kkt_registered(self._selected_kkt)
            logger.info(f"Статус после регистрации: {is_registered_now}")

            # Отправляем результат
            result = {
                'success': register_result.get('success', False),
                'step': 2,
                'tspiot_id': register_result.get('tspiot_id'),
                'message': 'Регистрация успешно завершена' if register_result.get('success')
                else f"Ошибка регистрации: {register_result.get('error_message')}",
                'is_registered': is_registered_now
            }

            logger.info(f"✅ Результат регистрации: {result}")
            self.registrationResultChanged.emit(result)

            # Обновляем статус кнопки
            self.registrationStatusChanged.emit()

        except Exception as e:
            logger.error(f"❌ Критическая ошибка регистрации: {e}", exc_info=True)
            self.registrationResultChanged.emit({
                'success': False,
                'message': f"Критическая ошибка: {e}"
            })
        finally:
            self._is_loading = False
            self.loadingChanged.emit()

    @Slot()
    def check_registration_status(self):
        """Принудительная проверка статуса регистрации (можно вызывать из QML)"""
        if self._selected_kkt:
            is_registered = self._tspiot_command.is_kkt_registered(self._selected_kkt)
            logger.info(f"🔍 Ручная проверка статуса для {self._selected_kkt}: {is_registered}")
            self.registrationStatusChanged.emit()
            return is_registered
        return False

    @Slot()
    def clear_selection(self):
        """Сбрасывает выбор"""
        logger.info("🧹 clear_selection()")
        self._selected_kkt = ""
        self._current_kkt_info = None
        self.selectedKktChanged.emit()
        self.kktInfoChanged.emit()
        self.registrationStatusChanged.emit()

    def close(self):
        """Закрывает соединения"""
        logger.info("🔒 Закрытие KKTController")
        if self._kkt_command:
            self._kkt_command.close()
        if self._tspiot_command:
            self._tspiot_command.close()

    def __del__(self):
        self.close()


class TSPIoTQmlLoader(QMainWindow):
    def __init__(self,
                 window_size: tuple,
                 app_icon_path: str,
                 header_name: str,
                 fonts_path: str,
                 qml_file: str,
                 use_test_data=True):
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
        engine.rootContext().setContextProperty("kktController", self._kkt_controller)
        logger.info("✅ Контроллер зарегистрирован в QML контексте как 'kktController'")

        # Загружаем QML
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
        self._kkt_controller.close()
        event.accept()


def main():
    # Параметры
    SRC_DIR = os.path.dirname(os.path.abspath(__file__))
    __WINDOW_SIZE = (700, 650)  # Немного увеличил для лучшего отображения
    __APP_HEADER_TITLE = "ТС ПИоТ - Управление кассами"
    __APP_ICON_PATH = os.path.join(SRC_DIR, "ui", "assets", "image_89.png")
    __FONTS_PATH = os.path.join(SRC_DIR, "ui", "fonts")
    __QML_PATH = os.path.join(SRC_DIR, "ui", "simple.qml")

    logger.info("=" * 50)
    logger.info("🚀 ЗАПУСК ПРИЛОЖЕНИЯ")
    logger.info("=" * 50)

    app = QApplication(sys.argv)

    # Создаем и показываем окно
    loader = TSPIoTQmlLoader(
        window_size=__WINDOW_SIZE,
        app_icon_path=__APP_ICON_PATH,
        header_name=__APP_HEADER_TITLE,
        fonts_path=__FONTS_PATH,
        qml_file=__QML_PATH,
        use_test_data=False  # Для тестирования можно менять
    )

    loader.show()

    # Периодическая проверка статуса регистрации (каждые 30 секунд)
    def periodic_status_check():
        if loader._kkt_controller._selected_kkt:
            loader._kkt_controller.check_registration_status()
        QTimer.singleShot(30000, periodic_status_check)

    QTimer.singleShot(30000, periodic_status_check)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()