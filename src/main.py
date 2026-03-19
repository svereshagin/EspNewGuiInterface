import os
import sys
import asyncio
import logging
from typing import List, Optional, Dict, Any
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from PySide6.QtCore import QObject, Slot, Property, Signal, QTimer, QUrl
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QMainWindow
from PySide6.QtQuickWidgets import QQuickWidget
from PySide6.QtGui import QFontDatabase, QIcon

# Импорты для ГИС МТ
from src.network.gismt import GisMtNetwork
from src.network.gismt import GisMtSettingsResponseDTO, GisMtSettingsUpdateDTO
from src.network.gismt import InstanceResponseDTO, InstancesListResponseDTO

# Импорты для ККТ
from src.domain.kkt.entity import CashInfo, ShiftState, KktInfo
from src.network.kkt import KKTNetwork
from src.network.controlmodule import ControlmoduleNetwork
from src.network.tspiot import TspiotSetup, RequestCreateInstanceTSPIOT_DTO, RequestRegistrationTSPIOT_DTO

# Импорты для ЛМ ЧЗ
from src.network.regime_local_module import (
    RegimeNetwork,
    RequestGetInfoRegime,
    RequestSetupRegime,
    ResponseGetInfoRegime,
    ResponseGetSettingsRegime
)

import resources_rc

def resource_path(relative_path):
    """Получить абсолютный путь к ресурсу, работает для dev и для PyInstaller"""
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)


# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app_debug.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# ==================== DTO ДЛЯ UI ====================

class GisMtSettingsInfo:
    """Информация о настройках ГИС МТ для отображения в UI"""

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
    """Информация об инстансе ГИС МТ для отображения в UI"""

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


# ==================== КОМАНДНЫЙ СЛОЙ ГИС МТ ====================

class GisMtCommands:
    """
    Командный слой для работы с ГИС МТ
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
            InstanceInfo(id="00106327428745", service_state="Работает", port=8080, created_at="2025-01-01T00:00:00"),
            InstanceInfo(id="00106327428746", service_state="Остановлен", port=8081, created_at="2025-01-02T00:00:00"),
            InstanceInfo(id="00234567890123", service_state="Работает", port=8082, created_at="2025-01-03T00:00:00")
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
        """Получает список всех инстансов"""
        logger.info("🔍 GisMtCommands.get_instances() вызван")
        try:
            loop = self._get_or_create_event_loop()
            instances = loop.run_until_complete(self._get_instances_async())
            logger.info(f"📋 Получено инстансов: {len(instances)}")
            return instances
        except Exception as e:
            logger.error(f"❌ Ошибка в get_instances: {e}")
            return []

    def get_instance_ids(self) -> List[str]:
        """Получает список ID всех инстансов"""
        instances = self.get_instances()
        return [inst.id for inst in instances]

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
        """Получает настройки драйвера ГИС МТ"""
        logger.info(f"🔍 get_settings для инстанса {instance_id}")
        try:
            loop = self._get_or_create_event_loop()
            settings = loop.run_until_complete(self._get_settings_async(instance_id))
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
        """Обновляет настройки драйвера ГИС МТ"""
        logger.info(f"🔧 update_settings для инстанса {instance_id}")
        try:
            loop = self._get_or_create_event_loop()
            result = loop.run_until_complete(
                self._update_settings_async(instance_id, compatibility_mode, allow_remote, gismt_address)
            )
            return result
        except Exception as e:
            logger.error(f"❌ Ошибка в update_settings: {e}")
            return False

    def close(self):
        """Закрывает соединения"""
        if self._network:
            try:
                loop = self._get_or_create_event_loop()
                if loop.is_running():
                    asyncio.create_task(self._network.close())
                else:
                    loop.run_until_complete(self._network.close())
            except Exception as e:
                logger.error(f"⚠️ Ошибка при закрытии: {e}")
        self._executor.shutdown(wait=False)


# ==================== КОМАНДНЫЙ СЛОЙ ККТ ====================

class KKTCommands:
    """Командный слой для работы с ККТ"""

    def __init__(self, use_test_data: bool = False):
        self._cached_result = None
        self._network = None
        self._loop = None
        self._executor = ThreadPoolExecutor(max_workers=1)
        self._use_test_data = use_test_data
        logger.info(f"🔧 KKTCommands инициализирован (test_data={use_test_data})")

    def _get_test_data(self) -> CashInfo:
        """Возвращает тестовые данные"""
        logger.info("🧪 Используем тестовые данные ККТ")
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
        """Возвращает список серийных номеров касс"""
        logger.info("🔍 KKTCommands.get_kkt_list() вызван")
        try:
            loop = self._get_or_create_event_loop()
            cash_info = loop.run_until_complete(self._get_kkt_list_async())

            if cash_info and cash_info.kkt:
                logger.info(f"📦 Получены данные: {len(cash_info.kkt)} касс")
                self._cached_result = cash_info
                return [kkt.kktSerial for kkt in cash_info.kkt]
            return []
        except Exception as e:
            logger.error(f"❌ Ошибка в get_kkt_list: {e}", exc_info=True)
            return []

    def get_full_kkt_info(self) -> Optional[CashInfo]:
        """Получает полную информацию о кассах"""
        logger.info("🔍 get_full_kkt_info() вызван")
        if self._cached_result:
            return self._cached_result
        try:
            loop = self._get_or_create_event_loop()
            cash_info = loop.run_until_complete(self._get_kkt_list_async())
            self._cached_result = cash_info
            return cash_info
        except Exception as e:
            logger.error(f"❌ Ошибка в get_full_kkt_info: {e}", exc_info=True)
            return None

    def close(self):
        """Закрывает соединения"""
        if self._network:
            try:
                loop = self._get_or_create_event_loop()
                if loop.is_running():
                    asyncio.create_task(self._network.close())
                else:
                    loop.run_until_complete(self._network.close())
            except Exception as e:
                logger.error(f"⚠️ Ошибка при закрытии: {e}")
        self._executor.shutdown(wait=False)


# ==================== КОМАНДНЫЙ СЛОЙ TSPIOT ====================

class TSPIOTCommands:
    """Командный слой для работы с TSPIOT - регистрация и создание экземпляров"""

    def __init__(self, use_test_data: bool = False):
        self._tspiot_setup = TspiotSetup()
        self._controlmodule_network = ControlmoduleNetwork()
        self._loop = None
        self._executor = ThreadPoolExecutor(max_workers=1)
        self._use_test_data = use_test_data
        logger.info("🔧 TSPIOTCommands инициализирован (test_data=%s)", use_test_data)

    def _get_or_create_event_loop(self):
        """Получает или создает event loop"""
        try:
            self._loop = asyncio.get_running_loop()
        except RuntimeError:
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
        return self._loop

    def get_cm_instances(self) -> List[str]:
        """Получает список ID зарегистрированных экземпляров ТС ПИоТ"""
        logger.debug("🔍 get_cm_instances() вызван")
        try:
            instances_dto = self._controlmodule_network._get_cm_instances()
            if instances_dto and instances_dto.instances:
                registered_ids = [inst.id for inst in instances_dto.instances]
                logger.info(f"📋 Получены зарегистрированные ID: {registered_ids}")
                return registered_ids
            return []
        except Exception as e:
            logger.error(f"❌ Ошибка получения экземпляров: {e}", exc_info=True)
            return []

    def is_kkt_registered(self, kkt_serial: str) -> bool:
        """Проверяет, зарегистрирована ли касса по серийному номеру"""
        logger.debug(f"🔍 Проверка регистрации кассы: {kkt_serial}")
        instances = self.get_cm_instances()
        is_registered = kkt_serial in instances
        logger.info(f"📊 Касса {kkt_serial} зарегистрирована: {is_registered}")
        return is_registered

    def create_esm_service(self, kkt_serial: str, port: int = None, soft_port: int = None) -> dict:
        """Создает экземпляр ESM сервиса"""
        logger.info(f"🔧 create_esm_service для {kkt_serial}")

        if self._use_test_data:
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
            result = self._tspiot_setup.create_esm_service(data)
            return {
                'success': result.success,
                'tspiot_id': result.tspiot_id,
                'status': result.status,
                'error_message': result.error_message
            }
        except Exception as e:
            logger.error(f"❌ Ошибка создания ESM: {e}", exc_info=True)
            return {'success': False, 'error_message': str(e)}

    def register_tspiot(self, instance_id: str, kkt_serial: str, fn_serial: str, kkt_inn: str) -> dict:
        """Регистрирует TSPIOT"""
        logger.info(f"🔧 register_tspiot для {kkt_serial}")

        if self._use_test_data:
            return {'success': True, 'tspiot_id': f"reg_{kkt_serial}"}

        try:
            data = RequestRegistrationTSPIOT_DTO(
                id=instance_id,
                kktSerial=kkt_serial,
                fnSerial=fn_serial,
                kktInn=kkt_inn
            )
            result = self._tspiot_setup.register_tspiot(data)
            if isinstance(result, dict) and 'success' in result:
                return result
            elif hasattr(result, 'tspiotId'):
                return {'success': True, 'tspiot_id': result.tspiotId}
            else:
                return {'success': False, 'error_message': "Неизвестный ответ от сервера"}
        except Exception as e:
            logger.error(f"❌ Ошибка регистрации: {e}", exc_info=True)
            return {'success': False, 'error_message': str(e)}

    def close(self):
        """Закрывает соединения"""
        logger.info("🔒 Закрытие TSPIOTCommands")
        if self._controlmodule_network:
            self._controlmodule_network.close()
        if self._loop and not self._loop.is_closed():
            self._loop.close()
            self._loop = None
        self._executor.shutdown(wait=False)


# ==================== КОМАНДНЫЙ СЛОЙ ЛМ ЧЗ ====================

class LMCommands:
    """Командный слой для работы с ЛМ ЧЗ"""

    def __init__(self, esm_instance_id: str, use_test_data: bool = False):
        self._esm_instance_id = esm_instance_id
        self._network = RegimeNetwork()
        self._use_test_data = use_test_data
        self._loop = None
        self._executor = ThreadPoolExecutor(max_workers=1)
        logger.info(f"🔧 LMCommands инициализирован для instance: {esm_instance_id} (test_data={use_test_data})")

    def _get_or_create_event_loop(self):
        """Получает или создает event loop"""
        try:
            self._loop = asyncio.get_running_loop()
        except RuntimeError:
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
        return self._loop

    def get_info(self) -> Optional[ResponseGetInfoRegime]:
        """Получает информацию о режиме"""
        logger.info("🔍 get_info вызван")
        try:
            info = self._network.get_regime_config_by_instance(
                RequestGetInfoRegime(esm_instance_id=self._esm_instance_id)
            )
            return info
        except Exception as e:
            logger.error(f"❌ Ошибка получения информации: {e}")
            return None

    def get_settings(self) -> Optional[ResponseGetSettingsRegime]:
        """Получает настройки"""
        logger.info("🔍 get_settings вызван")
        try:
            settings = self._network.get_regime_settings_by_instance(
                RequestGetInfoRegime(esm_instance_id=self._esm_instance_id)
            )
            return settings
        except Exception as e:
            logger.error(f"❌ Ошибка получения настроек: {e}")
            return None

    def save_settings(self, address: str, port: int, login: str, password: str) -> bool:
        """Сохраняет настройки"""
        logger.info(f"💾 save_settings: {address}:{port}")
        try:
            request = RequestSetupRegime(
                esm_instance_id=self._esm_instance_id,
                address=address,
                port=port,
                login=login,
                password=password
            )
            response = self._network.setup_regime_settings(request)
            return response and response.status_code == 200
        except Exception as e:
            logger.error(f"❌ Ошибка сохранения настроек: {e}")
            return False

    def close(self):
        """Закрывает соединения"""
        logger.info("🔒 Закрытие LMCommands")
        if self._network:
            self._network.close()
        self._executor.shutdown(wait=False)


# ==================== КОНТРОЛЛЕР ГИС МТ ====================

class GisMtController(QObject):
    """Контроллер для управления ГИС МТ в QML"""

    instancesListChanged = Signal()
    selectedInstanceChanged = Signal()
    settingsChanged = Signal()
    loadingChanged = Signal()
    errorOccurred = Signal(str)
    operationCompleted = Signal(dict)
    instancesLoaded = Signal(list)
    settingsLoaded = Signal(object)

    def __init__(self, parent=None, use_test_data: bool = False):
        super().__init__(parent)

        self._instances: List[str] = []
        self._instances_info: List[InstanceInfo] = []
        self._selected_instance: Optional[str] = None
        self._current_settings: Optional[GisMtSettingsInfo] = None
        self._is_loading = False
        self._operation_result: str = ""

        self._commands = GisMtCommands(use_test_data=use_test_data)

        self.instancesLoaded.connect(self._on_instances_loaded)
        self.settingsLoaded.connect(self._on_settings_loaded)

        logger.info(f"✅ GisMtController инициализирован (test_data={use_test_data})")
        QTimer.singleShot(500, self.refresh_instances)

    @Property(list, notify=instancesListChanged)
    def instances(self):
        return self._instances

    @Property(str, notify=selectedInstanceChanged)
    def selectedInstance(self):
        return self._selected_instance or ""

    @Property('QVariant', notify=settingsChanged)
    def currentSettings(self):
        if self._current_settings:
            return self._current_settings.to_dict()
        return None

    @Property(bool, notify=loadingChanged)
    def isLoading(self):
        return self._is_loading

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
        try:
            instances_info = self._commands.get_instances()
            self._instances_info = instances_info
            instance_ids = [inst.id for inst in instances_info]
            self.instancesLoaded.emit(instance_ids)
        except Exception as e:
            logger.error(f"❌ Ошибка в _refresh_instances_thread: {e}")
            self.errorOccurred.emit(str(e))
            self._is_loading = False
            self.loadingChanged.emit()

    @Slot(list)
    def _on_instances_loaded(self, instance_ids):
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

            from threading import Thread
            thread = Thread(target=self._load_settings_thread, args=(instance_id,))
            thread.daemon = True
            thread.start()

    def _load_settings_thread(self, instance_id: str):
        try:
            settings = self._commands.get_settings(instance_id)
            self.settingsLoaded.emit(settings)
        except Exception as e:
            logger.error(f"❌ Ошибка загрузки настроек: {e}")

    @Slot(object)
    def _on_settings_loaded(self, settings):
        self._current_settings = settings
        self.settingsChanged.emit()

    @Slot(bool, bool, str)
    def update_settings(self, compatibility_mode: bool, allow_remote: bool, gismt_address: str):
        """Обновляет настройки текущего инстанса"""
        if not self._selected_instance:
            return

        logger.info(f"📝 Обновление настроек для {self._selected_instance}")
        self._is_loading = True
        self.loadingChanged.emit()

        from threading import Thread
        thread = Thread(target=self._update_settings_thread, args=(
            self._selected_instance, compatibility_mode, allow_remote, gismt_address
        ))
        thread.daemon = True
        thread.start()

    def _update_settings_thread(self, instance_id: str, compatibility_mode: bool,
                                allow_remote: bool, gismt_address: str):
        try:
            success = self._commands.update_settings(
                instance_id=instance_id,
                compatibility_mode=compatibility_mode,
                allow_remote=allow_remote,
                gismt_address=gismt_address
            )
            result = {'success': success, 'message': 'Настройки обновлены' if success else 'Ошибка обновления'}
            if success:
                settings = self._commands.get_settings(instance_id)
                self.settingsLoaded.emit(settings)
            self.operationCompleted.emit(result)
        except Exception as e:
            logger.error(f"❌ Ошибка обновления: {e}")
            self.operationCompleted.emit({'success': False, 'message': str(e)})
        finally:
            self._is_loading = False
            self.loadingChanged.emit()

    def close(self):
        if self._commands:
            self._commands.close()


# ==================== КОНТРОЛЛЕР ККТ ====================

class KKTController(QObject):
    """Контроллер для управления кассами"""

    kktListChanged = Signal()
    selectedKktChanged = Signal()
    loadingChanged = Signal()
    kktInfoChanged = Signal()
    registrationStatusChanged = Signal()
    registrationResultChanged = Signal(dict)
    kktListUpdated = Signal(list)
    kktInfoUpdated = Signal(dict)

    def __init__(self, parent=None, use_test_data: bool = False):
        super().__init__(parent)
        logger.info(f"✅ KKTController инициализирован (test_data={use_test_data})")

        self._kkt_list = []
        self._selected_kkt = ""
        self._is_loading = False
        self._kkt_commands = KKTCommands(use_test_data=use_test_data)
        self._tspiot_commands = TSPIOTCommands(use_test_data=use_test_data)
        self._current_kkt_info = None

        self.kktListUpdated.connect(self._on_refresh_complete)
        self.kktInfoUpdated.connect(self._on_info_loaded)

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

    @Property('QVariant', notify=kktInfoChanged)
    def kktInfo(self):
        return self._current_kkt_info

    @Property(bool, notify=registrationStatusChanged)
    def canRegister(self):
        """Можно ли регистрировать выбранную кассу"""
        if not self._selected_kkt or not self._current_kkt_info:
            return False
        is_registered = self._tspiot_commands.is_kkt_registered(self._selected_kkt)
        return not is_registered

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
        try:
            new_kkt_list = self._kkt_commands.get_kkt_list()
            self.kktListUpdated.emit(new_kkt_list)
        except Exception as e:
            logger.error(f"❌ Ошибка в потоке обновления: {e}", exc_info=True)
            self.kktListUpdated.emit([])

    @Slot(list)
    def _on_refresh_complete(self, kkt_list):
        self._kkt_list = kkt_list
        self.kktListChanged.emit()
        self._is_loading = False
        self.loadingChanged.emit()
        if self._selected_kkt:
            self.registrationStatusChanged.emit()

    @Slot(str)
    def select_kkt(self, kkt_serial: str):
        """Выбирает кассу по серийному номеру"""
        logger.info(f"🎯 select_kkt({kkt_serial})")
        if self._selected_kkt != kkt_serial:
            self._selected_kkt = kkt_serial
            self.selectedKktChanged.emit()
            self.registrationStatusChanged.emit()

            from threading import Thread
            thread = Thread(target=self._load_kkt_info_thread, args=(kkt_serial,))
            thread.daemon = True
            thread.start()

    def _load_kkt_info_thread(self, kkt_serial: str):
        cash_info = self._kkt_commands.get_full_kkt_info()
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
                    self.kktInfoUpdated.emit(info_dict)
                    return
        self.kktInfoUpdated.emit(None)

    @Slot(dict)
    def _on_info_loaded(self, info_dict):
        self._current_kkt_info = info_dict
        self.kktInfoChanged.emit()
        if info_dict and self._selected_kkt:
            self.registrationStatusChanged.emit()

    @Slot()
    def register_current_kkt(self):
        """Регистрирует выбранную кассу"""
        if not self._selected_kkt or not self._current_kkt_info:
            logger.error("❌ Нет выбранной кассы для регистрации")
            return

        logger.info(f"📝 Начало регистрации кассы: {self._selected_kkt}")
        self._is_loading = True
        self.loadingChanged.emit()

        from threading import Thread
        thread = Thread(target=self._register_thread)
        thread.daemon = True
        thread.start()

    def _register_thread(self):
        try:
            # Шаг 1: Создаем ESM сервис
            create_result = self._tspiot_commands.create_esm_service(kkt_serial=self._selected_kkt)

            if not create_result.get('success'):
                error_msg = f"Ошибка создания ESM: {create_result.get('error_message')}"
                self.registrationResultChanged.emit({'success': False, 'message': error_msg})
                return

            tspiot_id = create_result.get('tspiot_id')

            # Шаг 2: Регистрируем TSPIOT
            register_result = self._tspiot_commands.register_tspiot(
                instance_id=tspiot_id,
                kkt_serial=self._current_kkt_info['kktSerial'],
                fn_serial=self._current_kkt_info['fnSerial'],
                kkt_inn=self._current_kkt_info['kktInn']
            )

            result = {
                'success': register_result.get('success', False),
                'message': 'Регистрация успешно завершена' if register_result.get('success')
                else f"Ошибка регистрации: {register_result.get('error_message')}"
            }
            self.registrationResultChanged.emit(result)
            self.registrationStatusChanged.emit()

        except Exception as e:
            logger.error(f"❌ Критическая ошибка регистрации: {e}", exc_info=True)
            self.registrationResultChanged.emit({'success': False, 'message': f"Критическая ошибка: {e}"})
        finally:
            self._is_loading = False
            self.loadingChanged.emit()

    @Slot()
    def check_registration_status(self):
        """Принудительная проверка статуса регистрации"""
        if self._selected_kkt:
            self._tspiot_commands.is_kkt_registered(self._selected_kkt)
            self.registrationStatusChanged.emit()

    def close(self):
        if self._kkt_commands:
            self._kkt_commands.close()
        if self._tspiot_commands:
            self._tspiot_commands.close()


# ==================== КОНТРОЛЛЕР ЛМ ЧЗ ====================

class LMController(QObject):
    """Контроллер для управления режимом ЛМ ЧЗ"""

    regimeInfoChanged = Signal()
    settingsChanged = Signal()
    loadingChanged = Signal()
    errorChanged = Signal()

    def __init__(self, esm_instance_id: str, parent=None, use_test_data: bool = False):
        super().__init__(parent)
        logger.info(f"✅ LMController инициализирован для instance: {esm_instance_id} (test_data={use_test_data})")

        self._esm_instance_id = esm_instance_id
        self._regime_info: Optional[ResponseGetInfoRegime] = None
        self._settings: Optional[ResponseGetSettingsRegime] = None
        self._is_loading = False
        self._error_message = ""

        self._commands = LMCommands(esm_instance_id, use_test_data=use_test_data)

        QTimer.singleShot(500, self.refresh_all)

    @Property(str, notify=regimeInfoChanged)
    def status(self) -> str:
        if self._regime_info and self._regime_info.lmStatus:
            status = self._regime_info.lmStatus.status
            operation_mode = self._regime_info.lmStatus.operationMode

            if status == "ready" and operation_mode == "active":
                return "🟢 Активен"
            elif status == "ready":
                return "🟡 Готов"
            else:
                return f"🔴 {status}"
        return "⚪ Неизвестно"

    @Property(str, notify=regimeInfoChanged)
    def version(self) -> str:
        if self._regime_info:
            return self._regime_info.controllerVersion
        return "—"

    @Property(str, notify=settingsChanged)
    def ip(self) -> str:
        if self._settings:
            return self._settings.address
        return "—"

    @Property(str, notify=regimeInfoChanged)
    def lastSync(self) -> str:
        if self._regime_info and self._regime_info.lmStatus:
            timestamp = self._regime_info.lmStatus.lastSync / 1000
            dt = datetime.fromtimestamp(timestamp)
            return dt.strftime("%d.%m.%Y %H:%M:%S")
        return "—"

    @Property(str, notify=regimeInfoChanged)
    def inn(self) -> str:
        if self._regime_info and self._regime_info.lmStatus:
            return self._regime_info.lmStatus.inn
        return "—"

    @Property(str, notify=settingsChanged)
    def login(self) -> str:
        if self._settings:
            return self._settings.login
        return "—"

    @Property(bool, notify=loadingChanged)
    def isLoading(self) -> bool:
        return self._is_loading

    @Property(str, notify=errorChanged)
    def errorMessage(self) -> str:
        return self._error_message

    @Slot()
    def refresh_all(self):
        """Обновляет все данные"""
        logger.info("🔄 refresh_all вызван")
        self._is_loading = True
        self.loadingChanged.emit()
        self.refresh_info()
        self.refresh_settings()

    @Slot()
    def refresh_info(self):
        """Обновляет информацию о режиме"""
        try:
            info = self._commands.get_info()
            if info:
                self._regime_info = info
                self._error_message = ""
            else:
                self._error_message = "Не удалось получить информацию"
        except Exception as e:
            self._error_message = f"Ошибка: {e}"
        finally:
            self.regimeInfoChanged.emit()
            self.errorChanged.emit()
            self._finish_loading_if_done()

    @Slot()
    def refresh_settings(self):
        """Обновляет настройки"""
        try:
            settings = self._commands.get_settings()
            if settings:
                self._settings = settings
            else:
                self._settings = ResponseGetSettingsRegime(address="", port=0, login="", password="")
        except Exception as e:
            logger.error(f"❌ Ошибка получения настроек: {e}")
        finally:
            self.settingsChanged.emit()
            self._finish_loading_if_done()

    @Slot(str, int, str, str)
    def save_settings(self, address: str, port: int, login: str, password: str):
        """Сохраняет настройки"""
        logger.info(f"💾 save_settings: {address}:{port}")
        self._is_loading = True
        self.loadingChanged.emit()

        try:
            success = self._commands.save_settings(address, port, login, password)
            if success:
                self._error_message = ""
                self.refresh_settings()
                self.refresh_info()
            else:
                self._error_message = "Ошибка при сохранении настроек"
        except Exception as e:
            self._error_message = f"Ошибка: {e}"
        finally:
            self.errorChanged.emit()
            self._is_loading = False
            self.loadingChanged.emit()

    def _finish_loading_if_done(self):
        """Завершает загрузку после обоих запросов"""
        QTimer.singleShot(1000, self._stop_loading)

    def _stop_loading(self):
        self._is_loading = False
        self.loadingChanged.emit()

    def close(self):
        if self._commands:
            self._commands.close()


# ==================== ГЛАВНЫЙ ЗАГРУЗЧИК QML ====================

class MainQmlLoader(QMainWindow):
    """Главный загрузчик QML со всеми контроллерами"""

    def __init__(self,
                 window_size: tuple,
                 app_icon_path: str,
                 header_name: str,
                 fonts_path: str,
                 qml_file: str,
                 use_test_data: bool = False,
                 lm_instance_id: str = "00106327428745"):
        super().__init__()

        # Создаем все контроллеры
        self._lm_controller = LMController(esm_instance_id=lm_instance_id, use_test_data=use_test_data)
        self._gismt_controller = GisMtController(use_test_data=use_test_data)
        self._kkt_controller = KKTController(use_test_data=use_test_data)

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
        engine = self.quick_widget.engine()

        # Регистрируем все контроллеры в контексте QML
        engine.rootContext().setContextProperty("lmController", self._lm_controller)
        engine.rootContext().setContextProperty("gisMtController", self._gismt_controller)
        engine.rootContext().setContextProperty("kktController", self._kkt_controller)
        logger.info("✅ Все контроллеры зарегистрированы в QML контексте")

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

        # Периодическая проверка статусов (каждые 30 секунд)
        QTimer.singleShot(30000, self.periodic_status_check)

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

    def periodic_status_check(self):
        """Периодическая проверка статусов"""
        if self._lm_controller:
            self._lm_controller.refresh_info()
        if self._gismt_controller and self._gismt_controller._selected_instance:
            self._gismt_controller.refresh_settings()
        if self._kkt_controller and self._kkt_controller._selected_kkt:
            self._kkt_controller.check_registration_status()
        QTimer.singleShot(30000, self.periodic_status_check)

    def closeEvent(self, event):
        """Обработка закрытия окна"""
        logger.info("🔒 Закрытие приложения")
        self._lm_controller.close()
        self._gismt_controller.close()
        self._kkt_controller.close()
        event.accept()


# ==================== ФУНКЦИЯ ПРОВЕРКИ РЕЖИМА КОМПИЛЯЦИИ ====================

def check_compile_mode():
    """Проверяет режим запуска (компиляция/разработка)"""
    if '--compiled' in sys.argv:
        sys.argv.remove('--compiled')
        return True
    if '--dev' in sys.argv:
        sys.argv.remove('--dev')
        return False
    return False


# ==================== ТОЧКА ВХОДА ====================

def main():
    """Главная функция запуска приложения"""
    use_compiled = check_compile_mode()
    use_test_data = False

    logger.info("=" * 50)
    logger.info("🚀 ЗАПУСК ГЛАВНОГО ПРИЛОЖЕНИЯ")
    logger.info("=" * 50)

    # Проверка режима запуска
    if getattr(sys, 'frozen', False):
        logger.info("📦 Запуск из скомпилированного приложения (frozen)")
        logger.info(f"📁 sys.executable: {sys.executable}")
        logger.info(f"📁 sys._MEIPASS: {sys._MEIPASS}")
    else:
        logger.info("💻 Запуск в режиме разработки")

    logger.info(f"🔧 Режим компиляции: {use_compiled}")
    logger.info(f"📊 Режим тестовых данных: {use_test_data}")

    # Параметры с использованием resource_path
    SRC_DIR = os.path.dirname(os.path.abspath(__file__))
    __WINDOW_SIZE = (900, 700)
    __APP_HEADER_TITLE = "Управление кассами и интеграциями"

    # Используем resource_path для всех файлов
    __APP_ICON_PATH = resource_path(os.path.join("src", "ui", "assets", "image_89.png"))
    __FONTS_PATH = resource_path(os.path.join("src", "ui", "fonts"))
    __QML_PATH = resource_path(os.path.join("src", "ui", "MainView.qml"))
    __LM_INSTANCE_ID = "00106327428745"

    # Проверяем существование файлов
    logger.info(f"📁 Проверка QML файла: {__QML_PATH} существует? {os.path.exists(__QML_PATH)}")
    logger.info(f"📁 Проверка папки со шрифтами: {__FONTS_PATH} существует? {os.path.exists(__FONTS_PATH)}")
    logger.info(f"📁 Проверка иконки: {__APP_ICON_PATH} существует? {os.path.exists(__APP_ICON_PATH)}")

    app = QApplication(sys.argv)

    # Создаем и показываем главное окно
    loader = MainQmlLoader(
        window_size=__WINDOW_SIZE,
        app_icon_path=__APP_ICON_PATH,
        header_name=__APP_HEADER_TITLE,
        fonts_path=__FONTS_PATH,
        qml_file=__QML_PATH,
        use_test_data=use_test_data,
        lm_instance_id=__LM_INSTANCE_ID
    )

    loader.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()