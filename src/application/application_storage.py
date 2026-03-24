from PySide6.QtCore import QObject, Signal, Slot, Property, QTimer, Qt, QRunnable, QThreadPool, QThread
from typing import Optional, List, Dict, Any
from datetime import datetime
import time

import logging
from PySide6.QtCore import Qt
from src.network.controlmodule import ControlmoduleNetwork, SystemsStatusResponseDTO
from src.network.gismt import GisMtNetwork, GisMtSettingsResponseDTO, GisMtSettingsUpdateDTO
from src.network.kkt import KKTNetwork
from src.network.regime_local_module import (
    RegimeNetwork,
    RequestGetInfoRegime,
    RequestSetupRegime,
    ResponseGetInfoRegime,
    ResponseGetSettingsRegime
)
from src.network.tspiot import TspiotSetup, RequestCreateInstanceTSPIOT_DTO, RequestRegistrationTSPIOT_DTO, \
    TspiotResult, ResponseRegistrationTSPIOT_DTO
from src.domain.kkt.entity import CashInfo, KktInfo

logger = logging.getLogger(__name__)


REGISTRATION_CACHE_TTL = 55



class RegistrationWorker(QThread):
    """Поток для регистрации ККТ"""
    finished = Signal(dict)
    progress = Signal(str)  # для статуса

    def __init__(self, tspiot_setup, kkt_serial, fn_serial, kkt_inn):
        super().__init__()
        self._tspiot_setup = tspiot_setup
        self.kkt_serial = kkt_serial
        self.fn_serial = fn_serial
        self.kkt_inn = kkt_inn
        self._is_cancelled = False

    def cancel(self):
        self._is_cancelled = True


    def _register_esm_tspiot(self):
        self.progress.emit("Регистрация TSPIOT...")
        register_data = RequestRegistrationTSPIOT_DTO(
            id=self.kkt_serial,
            kktSerial=self.kkt_serial,
            fnSerial=self.fn_serial,
            kktInn=self.kkt_inn
        )
        register_result: ResponseRegistrationTSPIOT_DTO = self._tspiot_setup.register_tspiot(register_data)
        if register_result.result:
            logger.info("Регистрация прошла успешно")
            self.finished.emit({
                'success': True,
                'message': 'Регистрация успешно завершена',
                'kkt_serial': self.kkt_serial
            })
        else:
            logger.info()
            logger.info("Регистрация прошла с ошибкой")
            self.finished.emit({
                'success': False,
                'message': f"Ошибка регистрации: {error}",
                'kkt_serial': self.kkt_serial
            })

    def run(self):
        try:
            self.progress.emit("Создание ESM сервиса...")
            if self._is_cancelled:
                self.finished.emit({'success': False, 'message': 'Отменено пользователем'})
                return

            logger.info("Начинаем создание инстанса для tspiot")
            create_data = RequestCreateInstanceTSPIOT_DTO(kkt_serial=self.kkt_serial)
            create_esm_service_result: TspiotResult = self._tspiot_setup.create_esm_service(create_data)

            if create_esm_service_result.success:
                logger.info("Создали инстанс ESM, переходим к регистрации")
                self._register_esm_tspiot()

            if not create_esm_service_result.success and create_esm_service_result.status == "Уже существует":
                self.progress.emit("ESM уже существует, получаем ID...")
                logger.info("Получили 1010, инстанс создан но не зареган, пытаемся ещё раз зарегать")
                self._register_esm_tspiot()


            elif not create_esm_service_result.success:
                self.finished.emit({
                    'success': False,
                    'message': f"Ошибка создания ESM: {create_esm_service_result.error_message}"
                })
                return

            self.progress.emit("Регистрация TSPIOT...")


        except Exception as e:
            self.finished.emit({
                'success': False,
                'message': f"Ошибка: {e}",
                'kkt_serial': self.kkt_serial
            })




class AsyncWorker(QRunnable):
    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    def run(self):
        try:
            result = self.func(*self.args, **self.kwargs)
            self.signals.result.emit(result)
        except Exception as e:
            self.signals.error.emit(e)

class WorkerSignals(QObject):
    result = Signal(object)
    error = Signal(Exception)


class ApplicationStorage(QObject):
    """
    Хранилище состояния приложения.
    Содержит всю бизнес-логику и данные.
    """

    # Сигналы
    uiReady = Signal()

    currentKktChanged = Signal(str)
    kktListChanged = Signal(list)
    lmStatusChanged = Signal()
    gismtStatusChanged = Signal()
    loadingChanged = Signal(bool)
    errorOccurred = Signal(str)
    statusUpdated = Signal(dict)
    licenseInfoChanged = Signal()
    registrationStatusChanged = Signal(str, bool)

    registrationCompleted = Signal(dict)
    registrationProgress = Signal(str)


    kktInfoUpdated = Signal(dict)
    def __init__(self, parent=None):
        super().__init__(parent)

        #старт сигналов после загрузки приложения
        self.uiReady.connect(self._on_ui_ready, Qt.ConnectionType.QueuedConnection)

        self._registration_cache: Dict[str, tuple] = {}
        self._pending_registration_checks: set = set()


        # Сетевые клиенты
        self._controlmodule_network = ControlmoduleNetwork()
        self._gismt_network = GisMtNetwork()
        self._kkt_network = KKTNetwork()
        self._regime_network = RegimeNetwork()
        self._tspiot_setup = TspiotSetup()


        self.threadpool = QThreadPool()


        # Данные о текущем состоянии
        self._current_kkt: Optional[str] = None
        self._kkt_list: List[str] = []
        self._is_loading: bool = False

        # Статусы конфигурации
        self._is_configured_lm_cz: bool = False
        self._is_configured_gismt: bool = False

        # Ошибки и последние соединения
        self._lm_error: str = ""
        self._lm_last_connection: str = ""
        self._gismt_error: str = ""
        self._gismt_last_connection: str = ""

        # Дополнительная информация о ЛМ
        self._lm_version: str = ""
        self._lm_status_text: str = ""
        self._lm_inn: str = ""
        self._lm_ip: str = "127.0.0.1"
        self._lm_login: str = "admin"
        self._lm_password: str = "admin"
        self._lm_port: int = 0



        # Дополнительная информация о ГИС МТ
        self._gismt_status_text: str = ""

        # Информация о лицензии ГИС МТ
        self._license_active: bool = False
        self._license_active_till: str = "—"
        self._license_last_sync: str = "—"
        self._license_state: str = "—"
        self._license_version: str = ""

        # Настройки ГИС МТ
        self._gismt_settings: Optional[Dict[str, Any]] = None

        # Информация о ККТ
        self._kkt_info_cache: Dict[str, Dict[str, Any]] = {}

        logger.info("✅ ApplicationStorage инициализирован")
        self._registration_timer = QTimer()
        self._registration_timer.timeout.connect(self._periodic_registration_check)
        # Загружаем список ККТ при старте

    @Slot()
    def notify_ui_ready(self):
        """Вызывается из QML когда UI готов"""
        logger.info("📢 UI сообщил о готовности")
        self.uiReady.emit()

    @Slot()
    def _on_ui_ready(self):
        """Запускаем загрузку данных после готовности UI"""
        logger.info("🚀 Запуск загрузки данных после готовности UI")
        self.refresh_kkt_list()
        # Запускаем таймер только после готовности UI
        self._registration_timer.start(60000)


    # ==================== Свойства для QML ====================
    def _periodic_registration_check(self):
        """Периодическая проверка статуса регистрации"""
        logger.debug("🔄 Периодическая проверка статуса регистрации")
        if self._current_kkt:
            self._update_registration_status(self._current_kkt)


    @property
    def lmIp(self) -> str:
        """IP адрес ЛМ ЧЗ"""
        return self._lm_ip

    def emit_registration_status(self, kkt_serial: str):
        """Отправляет актуальный статус регистрации"""
        is_registered = self.check_kkt_registration(kkt_serial)
        self.registrationStatusChanged.emit(kkt_serial, is_registered)

    @property
    def lmLogin(self) -> str:
        """Логин ЛМ ЧЗ"""
        return self._lm_login

    @property
    def lmPassword(self) -> str:
        """Логин ЛМ ЧЗ"""
        return self._lm_password


    @property
    def lmPort(self) -> int:
        """Порт ЛМ ЧЗ"""
        return self._lm_port


    @Property(str, notify=currentKktChanged)
    def currentKkt(self) -> str:
        return self._current_kkt or ""

    @Property(list, notify=kktListChanged)
    def kktList(self) -> list:
        return self._kkt_list

    @Property(bool, notify=loadingChanged)
    def isLoading(self) -> bool:
        return self._is_loading

    @Property(bool, notify=lmStatusChanged)
    def isLmConfigured(self) -> bool:
        return self._is_configured_lm_cz

    @Property(bool, notify=gismtStatusChanged)
    def isGismtConfigured(self) -> bool:
        return self._is_configured_gismt

    @Property(str, notify=lmStatusChanged)
    def lmError(self) -> str:
        return self._lm_error

    @Property(str, notify=lmStatusChanged)
    def lmLastConnection(self) -> str:
        return self._lm_last_connection

    @Property(str, notify=lmStatusChanged)
    def lmVersion(self) -> str:
        return self._lm_version

    @Property(str, notify=lmStatusChanged)
    def lmStatusText(self) -> str:
        return self._lm_status_text

    @Property(str, notify=lmStatusChanged)
    def lmInn(self) -> str:
        return self._lm_inn

    @Property(str, notify=gismtStatusChanged)
    def gismtError(self) -> str:
        return self._gismt_error

    @Property(str, notify=gismtStatusChanged)
    def gismtLastConnection(self) -> str:
        return self._gismt_last_connection

    @Property(str, notify=gismtStatusChanged)
    def gismtStatusText(self) -> str:
        return self._gismt_status_text

    @Property(bool, notify=licenseInfoChanged)
    def licenseActive(self) -> bool:
        return self._license_active

    @Property(str, notify=licenseInfoChanged)
    def licenseActiveTill(self) -> str:
        return self._license_active_till

    @Property(str, notify=licenseInfoChanged)
    def licenseLastSync(self) -> str:
        return self._license_last_sync

    @Property(str, notify=licenseInfoChanged)
    def licenseState(self) -> str:
        return self._license_state

    @Property(str, notify=licenseInfoChanged)
    def licenseVersion(self) -> str:
        return self._license_version

    @Property('QVariant', notify=gismtStatusChanged)
    def gismtSettings(self) -> dict:
        return self._gismt_settings or {}

    # ==================== Методы для работы с ККТ ====================

    @Slot()
    def refresh_kkt_list(self):
        """Обновляет список доступных ККТ через KKTNetwork"""
        logger.info("🔄 Обновление списка ККТ")
        self._set_loading(True)

        def fetch_kkt_list():
            import asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                # Таймаут прямо на уровне корутины
                return loop.run_until_complete(
                    asyncio.wait_for(self._kkt_network.get_dkktList(), timeout=60.0)
                )
            finally:
                loop.close()

        worker = AsyncWorker(fetch_kkt_list)
        worker.signals.result.connect(self._on_kkt_list_fetched)
        worker.signals.error.connect(self._on_kkt_list_error)
        self.threadpool.start(worker)

    def _on_kkt_list_fetched(self, cash_info):
        """Обрабатывает результат получения списка ККТ (вызывается в главном потоке)"""
        try:
            self._registration_cache.clear()
            if cash_info and cash_info.kkt:
                self._kkt_list = [kkt.kktSerial for kkt in cash_info.kkt]
                logger.info(f"📋 Найдено ККТ: {len(self._kkt_list)}")

                for kkt in cash_info.kkt:
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
                    self._kkt_info_cache[kkt.kktSerial] = info_dict

                    self._update_registration_status(kkt.kktSerial)

                if not self._current_kkt and self._kkt_list:
                    self.set_current_kkt(self._kkt_list[0])
            else:
                self._kkt_list = []
                logger.warning("⚠️ Нет доступных ККТ")
                self.errorOccurred.emit("Кассы не найдены")

            self.kktListChanged.emit(self._kkt_list)

        except Exception as e:
            logger.error(f"❌ Ошибка обработки списка ККТ: {e}")
            self.errorOccurred.emit(f"Ошибка: {e}")
        finally:
            self._set_loading(False)

    def _on_kkt_list_error(self, error: Exception):
        """Обрабатывает ошибку получения списка ККТ"""
        logger.error(f"❌ Ошибка получения списка ККТ: {error}")

        # Различаем таймаут и другие ошибки
        import asyncio
        if isinstance(error, asyncio.TimeoutError):
            msg = "ККТ не загружены: превышено время ожидания ответа от сервера (60 сек)"
        elif "connect" in str(error).lower():
            msg = "ККТ не загружены: нет соединения с сервером"
        else:
            msg = f"ККТ не загружены: {type(error).__name__}"

        logger.error(f"❌ {msg}")
        self._kkt_list = []
        self.kktListChanged.emit(self._kkt_list)
        self.errorOccurred.emit(msg)
        self._set_loading(False)

    @Slot(str)
    def set_current_kkt(self, kkt_id: str):
        """Устанавливает текущий ККТ"""
        if not kkt_id:
            logger.warning("⚠️ Попытка выбрать пустой ККТ")
            return

        if self._current_kkt != kkt_id:
            logger.info(f"🎯 Выбран ККТ: {kkt_id}")
            self._current_kkt = kkt_id
            self.currentKktChanged.emit(kkt_id)

            # Загружаем информацию о ККТ
            self._load_kkt_info(kkt_id)

            # Обновляем статус для выбранного ККТ
            self.get_application_status()

    def _load_kkt_info(self, kkt_serial: str):
        """Загружает детальную информацию о ККТ"""
        logger.info(f"🔍 Загрузка информации о ККТ: {kkt_serial}")

        # Проверяем кэш
        if kkt_serial in self._kkt_info_cache:
            logger.info(f"📦 Используем кэшированную информацию для {kkt_serial}")
            self.kktInfoUpdated.emit(self._kkt_info_cache[kkt_serial])
            return

        def fetch_kkt_info():
            import asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                cash_info = loop.run_until_complete(
                    asyncio.wait_for(self._kkt_network.get_dkktList(), timeout=60.0)
                )
                if cash_info and cash_info.kkt:
                    for kkt in cash_info.kkt:
                        if kkt.kktSerial == kkt_serial:
                            return {
                                'kktSerial': kkt.kktSerial,
                                'fnSerial': kkt.fnSerial,
                                'kktInn': kkt.kktInn,
                                'kktRnm': kkt.kktRnm,
                                'modelName': kkt.modelName,
                                'dkktVersion': kkt.dkktVersion,
                                'developer': kkt.developer,
                                'manufacturer': kkt.manufacturer,
                                'shiftState': kkt.shiftState.value if hasattr(kkt.shiftState, 'value') else str(
                                    kkt.shiftState)
                            }
                return None
            finally:
                loop.close()

        worker = AsyncWorker(fetch_kkt_info)
        worker.signals.result.connect(
            lambda info: self._on_kkt_info_fetched(kkt_serial, info)
        )
        worker.signals.error.connect(
            lambda err: self._on_kkt_info_error(kkt_serial, err)
        )
        self.threadpool.start(worker)

    def _on_kkt_info_fetched(self, kkt_serial: str, info_dict):
        """Обрабатывает результат загрузки информации о ККТ"""
        if info_dict:
            self._kkt_info_cache[kkt_serial] = info_dict
            self.kktInfoUpdated.emit(info_dict)
            logger.info(f"✅ Информация о ККТ {kkt_serial} загружена")
        else:
            logger.warning(f"⚠️ Касса {kkt_serial} не найдена в списке")
            self.errorOccurred.emit(f"Касса {kkt_serial} не найдена")

    def _on_kkt_info_error(self, kkt_serial: str, error: Exception):
        import asyncio
        if isinstance(error, asyncio.TimeoutError):
            msg = f"Не удалось загрузить данные кассы {kkt_serial}: превышено время ожидания"
        elif "connect" in str(error).lower():
            msg = f"Не удалось загрузить данные кассы {kkt_serial}: нет соединения с сервером"
        else:
            msg = f"Не удалось загрузить данные кассы {kkt_serial}: {error}"

        logger.error(f"❌ {msg}")
        self.errorOccurred.emit(msg)


    def get_kkt_info(self, kkt_serial: str) -> Optional[Dict[str, Any]]:
        """Возвращает информацию о ККТ"""
        return self._kkt_info_cache.get(kkt_serial)

    @Slot(result=dict)
    def get_current_kkt_info(self) -> dict:
        """Возвращает информацию о текущем ККТ"""
        if self._current_kkt and self._current_kkt in self._kkt_info_cache:
            return self._kkt_info_cache[self._current_kkt]
        return {}

    def _update_registration_status(self, kkt_serial: str):
        if not kkt_serial:
            return

        # Уже есть активный воркер для этой кассы — не запускаем дубль
        if kkt_serial in self._pending_registration_checks:
            return

        cache_entry = self._registration_cache.get(kkt_serial)
        if cache_entry:
            cache_time, cached_value = cache_entry
            if time.time() - cache_time < REGISTRATION_CACHE_TTL:
                self.registrationStatusChanged.emit(kkt_serial, cached_value)
                return

        self._pending_registration_checks.add(kkt_serial)

        def check_reg():
            try:
                instances = self._controlmodule_network._get_cm_instances()
                if instances and instances.instances:
                    registered_ids = [inst.id for inst in instances.instances]
                    return kkt_serial in registered_ids
                return False
            except Exception as e:
                logger.error(f"❌ Ошибка: {e}")
                return False

        worker = AsyncWorker(check_reg)
        worker.signals.result.connect(
            lambda is_reg: self._on_registration_checked(kkt_serial, is_reg)
        )
        self.threadpool.start(worker)

    def _on_registration_checked(self, kkt_serial: str, is_registered: bool):
        self._pending_registration_checks.discard(kkt_serial)  # ← убираем из pending
        self._registration_cache[kkt_serial] = (time.time(), is_registered)
        self.registrationStatusChanged.emit(kkt_serial, is_registered)
        logger.info(f"📊 Касса {kkt_serial} зарегистрирована: {is_registered}")
    # ==================== Получение статуса ====================

    @Slot()
    def get_application_status(self):
        """Получает статус приложения для текущего ККТ"""
        if not self._current_kkt:
            logger.warning("⚠️ Не выбран ККТ для получения статуса")
            return

        logger.info(f"🔍 Получение статуса для ККТ: {self._current_kkt}")
        self._set_loading(True)

        try:
            result = self._controlmodule_network.get_systems_status(self._current_kkt)
            logger.info(result)

            if result:
                self._process_status_result(result)
            elif result is None:
                logger.error(f"❌ 204 ошибка, не найдено ")
            else:
                logger.error(f"❌ Не удалось получить статус для {self._current_kkt}")
                self.errorOccurred.emit("Не удалось получить статус системы")

        except Exception as e:
            logger.error(f"❌ Ошибка получения статуса: {e}")
            self.errorOccurred.emit(f"Ошибка: {e}")
        finally:
            self._set_loading(False)

    def _process_status_result(self, result: SystemsStatusResponseDTO):
        """Обрабатывает результат получения статуса"""

        # Обновляем статусы конфигурации
        if result.all_systems_ok:
            self._is_configured_lm_cz = True
            self._is_configured_gismt = True
            self._lm_error = ""
            self._gismt_error = ""
            self._lm_status_text = "Подключено"
            self._gismt_status_text = "Подключено"
        else:
            # ГИС МТ
            if result.gismt.code == 0:
                self._is_configured_gismt = True
                self._gismt_error = ""
                self._gismt_status_text = "Подключено"
            elif result.gismt.code == 1:
                self._is_configured_gismt = True
                self._gismt_error = result.gismt.error
                self._gismt_status_text = f"Ошибка: {result.gismt.error}"
            else:
                self._is_configured_gismt = False
                self._gismt_error = result.gismt.error
                self._gismt_status_text = "Не подключено"

            # ЛМ ЧЗ
            if result.lm.code == 0:
                self._is_configured_lm_cz = True
                self._lm_error = ""
                self._lm_status_text = "Подключено"
            elif result.lm.code == 1:
                self._is_configured_lm_cz = True
                self._lm_error = result.lm.error
                self._lm_status_text = f"Ошибка: {result.lm.error}"
            else:
                self._is_configured_lm_cz = False
                self._lm_error = result.lm.error
                self._lm_status_text = "Не подключено"

        # ===== НОВЫЙ КОД: Обновляем статус лицензии на основе статуса ГИС МТ =====
        was_license_active = self._license_active

        # Если ГИС МТ подключен (код 0), то лицензия активна
        if result.gismt.code == 0:
            self._license_active = True
            self._license_state = "Активна"
            if not was_license_active:
                logger.info("✅ Лицензия ГИС МТ активирована (на основе статуса системы)")
        else:
            self._license_active = False
            self._license_state = "Неактивна"
            if was_license_active:
                logger.warning(f"❌ Лицензия ГИС МТ деактивирована. Статус: {result.gismt.code}")

        # Обновляем время последнего соединения
        self._gismt_last_connection = result.gismt.lastConnection
        self._lm_last_connection = result.lm.lastConnection

        # Отправляем сигналы об изменениях
        self.lmStatusChanged.emit()
        self.gismtStatusChanged.emit()

        # Отправляем сигнал об изменении лицензии, если статус изменился
        if was_license_active != self._license_active:
            self.licenseInfoChanged.emit()

        # Отправляем общий статус
        status_dict = {
            'gismt': {
                'code': result.gismt.code,
                'status': self._gismt_status_text,
                'lastConnection': self._gismt_last_connection,
                'error': self._gismt_error,
                'licenseActive': self._license_active  # Добавляем статус лицензии
            },
            'lm': {
                'code': result.lm.code,
                'status': self._lm_status_text,
                'lastConnection': self._lm_last_connection,
                'error': self._lm_error
            },
            'allOk': result.all_systems_ok
        }
        self.statusUpdated.emit(status_dict)

        # Загружаем детальную информацию о ЛМ
        self._load_lm_details()

    def _load_lm_details(self):
        """Загружает детальную информацию о ЛМ ЧЗ"""
        if not self._current_kkt:
            return

        try:
            # Получаем информацию о конфигурации ЛМ
            request = RequestGetInfoRegime(esm_instance_id=self._current_kkt)
            lm_info = self._regime_network.get_regime_config_by_instance(request)

            if lm_info and hasattr(lm_info, 'lmStatus'):
                self._lm_version = getattr(lm_info, 'controllerVersion', '')
                if hasattr(lm_info.lmStatus, 'inn'):
                    self._lm_inn = lm_info.lmStatus.inn
                self.lmStatusChanged.emit()

            # Получаем настройки подключения к ЛМ
            settings = self._regime_network.get_regime_settings_by_instance(
                RequestGetInfoRegime(esm_instance_id=self._current_kkt)
            )

            if settings:
                self._lm_ip = settings.address
                self._lm_port = settings.port
                self._lm_login = settings.login
                self._lm_password = settings.password
                logger.info(f"📋 Настройки ЛМ: {self._lm_ip}:{self._lm_port}, логин: {self._lm_login}, пароль: {self._lm_password}")
                self.lmStatusChanged.emit()  # Обновляем UI

        except Exception as e:
            logger.error(f"❌ Ошибка загрузки детальной информации ЛМ: {e}")
    # ==================== Настройки ГИС МТ ====================

    def _load_gismt_settings(self, instance_id: str):
        """Загружает настройки ГИС МТ для указанного инстанса"""
        logger.info(f"🔍 Загрузка настроек ГИС МТ для {instance_id}")

        try:
            settings = self._gismt_network.get_settings(instance_id)
            if settings:
                self._process_gismt_settings(instance_id, settings)
        except Exception as e:
            logger.error(f"❌ Ошибка загрузки настроек ГИС МТ: {e}")

    def _process_gismt_settings(self, instance_id: str, settings):
        """Обрабатывает настройки ГИС МТ"""
        self._gismt_settings = {
            'instanceId': instance_id,
            'compatibilityMode': settings.compatibilityMode,
            'allowRemote': settings.allowRemoteConnection,
            'gismtAddress': settings.gismtAddress
        }


        if hasattr(settings, 'licenses') and settings.licenses:
            license_data = settings.licenses[0]
            active_till = license_data.get('activeTill', '')
            if active_till:
                try:
                    if ' ' in active_till:
                        dt = datetime.strptime(active_till, '%Y-%m-%d %H:%M:%S')
                    else:
                        dt = datetime.strptime(active_till, '%Y-%m-%d')
                    self._license_active_till = dt.strftime('%d.%m.%Y')
                except Exception as e:
                    logger.warning(f"⚠️ Ошибка парсинга даты activeTill: {e}")
                    self._license_active_till = active_till

            last_sync = license_data.get('lastSync', '')
            if last_sync:
                try:
                    if ' ' in last_sync:
                        dt = datetime.strptime(last_sync, '%Y-%m-%d %H:%M:%S')
                    else:
                        dt = datetime.strptime(last_sync, '%Y-%m-%d')
                    self._license_last_sync = dt.strftime('%d.%m.%Y %H:%M')
                except Exception as e:
                    logger.warning(f"⚠️ Ошибка парсинга даты lastSync: {e}")
                    self._license_last_sync = last_sync

            self._license_version = license_data.get('version', '—')
            # Не обновляем _license_state здесь, он обновляется в _process_status_result

            logger.info(
                f"📄 Данные лицензии из API: версия={self._license_version}, действует до={self._license_active_till}")
            # Не вызываем licenseInfoChanged.emit() здесь, так как статус еще не определен
        else:
            # Если нет данных о лицензии, оставляем текущие значения
            pass

        self.gismtStatusChanged.emit()

    @Slot(str, bool, bool, str, result=bool)
    def update_gismt_settings(self, instance_id: str, compatibility_mode: bool,
                              allow_remote: bool, gismt_address: str) -> bool:
        """Обновляет настройки ГИС МТ"""
        logger.info(f"📝 Обновление настроек ГИС МТ для {instance_id}")
        self._set_loading(True)

        try:
            update_dto = GisMtSettingsUpdateDTO(
                compatibilityMode=compatibility_mode,
                allowRemoteConnection=allow_remote,
                gismtAddress=gismt_address
            )
            result = self._gismt_network.update_settings(instance_id, update_dto)

            if result:
                logger.info("✅ Настройки ГИС МТ обновлены")
                # Перезагружаем настройки
                self._load_gismt_settings(instance_id)
                # Обновляем статус
                self.get_application_status()
            else:
                logger.error("❌ Ошибка обновления настроек ГИС МТ")

            return result

        except Exception as e:
            logger.error(f"❌ Ошибка: {e}")
            return False
        finally:
            self._set_loading(False)

    # ==================== Настройки ЛМ ЧЗ ====================

    @Slot(str, int, str, str, result=bool)
    def update_lm_settings(self, address: str, port: int, login: str, password: str) -> bool:
        """Обновляет настройки подключения к ЛМ ЧЗ"""
        if not self._current_kkt:
            logger.error("❌ Не выбран ККТ для обновления настроек ЛМ")
            return False

        logger.info(f"📝 Обновление настроек ЛМ для {self._current_kkt}")
        self._set_loading(True)

        address = address or "127.0.0.1"
        port = port or 50063
        login = login or "admin"
        password = password or "admin"

        try:
            request = RequestSetupRegime(
                esm_instance_id=self._current_kkt,
                address=address,
                port=port,
                login=login,
                password=password
            )
            response = self._regime_network.setup_regime_settings(request)

            success = response and response.status_code == 200
            if success:
                logger.info("✅ Настройки ЛМ обновлены")
                self.get_application_status()
            else:
                logger.error("❌ Ошибка обновления настроек ЛМ")

            return success

        except Exception as e:
            logger.error(f"❌ Ошибка: {e}")
            return False
        finally:
            self._set_loading(False)

    # ==================== Регистрация ККТ ====================

    @Slot(str, str, str)
    def register_kkt(self, kkt_serial: str, fn_serial: str, kkt_inn: str):
        """Асинхронная регистрация"""
        self._set_loading(True)

        self._registration_worker = RegistrationWorker(
            self._tspiot_setup, kkt_serial, fn_serial, kkt_inn
        )
        self._registration_worker.finished.connect(self._on_registration_finished)
        self._registration_worker.progress.connect(self.registrationProgress.emit)
        self._registration_worker.start()




    def _on_registration_finished(self, result: dict):
        self._set_loading(False)
        self.registrationCompleted.emit(result)

        if result.get('kkt_serial'):
            # Инвалидируем кэш принудительно — пользователь только что что-то сделал
            self._registration_cache.pop(result['kkt_serial'], None)
            self._pending_registration_checks.discard(result['kkt_serial'])
            # Теперь следующий вызов гарантированно пойдёт на сервер
            self._update_registration_status(result['kkt_serial'])

    # ==================== Вспомогательные методы ====================

    def _set_loading(self, loading: bool):
        """Устанавливает флаг загрузки"""
        if self._is_loading != loading:
            self._is_loading = loading
            self.loadingChanged.emit(loading)

    # ==================== Закрытие ресурсов ====================

    @Slot(str, result=bool)
    def check_kkt_registration(self, kkt_serial: str) -> bool:
        """Проверяет, зарегистрирована ли касса (читает кэш)"""
        cache_entry = self._registration_cache.get(kkt_serial)
        if cache_entry:
            cache_time, cached_value = cache_entry
            if time.time() - cache_time < REGISTRATION_CACHE_TTL:
                return cached_value

        # Если кэша нет, запускаем фоновую проверку
        self._update_registration_status(kkt_serial)
        return False

    def close(self):
        """Закрывает все соединения"""
        logger.info("🔒 Закрытие ApplicationStorage")
        # Исправляем имена атрибутов
        if hasattr(self, '_controlmodule_network'):
            self._controlmodule_network.close()
        if hasattr(self, '_gismt_network'):
            self._gismt_network.close()
        if hasattr(self, '_kkt_network'):
            self._kkt_network.close()
        if hasattr(self, '_regime_network'):
            self._regime_network.close()