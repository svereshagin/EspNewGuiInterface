# storage/app_storage.py
import logging
from typing import Optional, Dict, List
from PySide6.QtCore import QObject, Signal

from dto.tspiot import TSPIoTInstancesResponseDTO, TSPIoTInstanceInfoDTO, TSPIoTSystemsStatusResponseDTO
from src.dto.kkt import CashInfo, KktInfo
from src.services.kkt_service import KKTService
from src.storage.async_executor import AsyncExecutor
from src.storage.cache_manager import CacheManager
from src.storage.mappers.kkt_mapper import KktMapper
from src.services.tspiot import TSPIoTService

logger =  logging.getLogger(__name__)

class AppStorage(QObject):
    """Хранилище состояния - только бизнес-логика"""

    #KKT
    kktListChanged = Signal()
    currentSerialChanged = Signal()

    #ANY API SIGNALS [СЛЕДИМ ЗА ПРОЦЕССАМИ]
    loadingChanged = Signal(bool)  # Пробрасываем от AsyncExecutor
    errorChanged = Signal(str)  # Пробрасываем от AsyncExecutor

    instancesListChanged = Signal()
    currentInstanceChanged = Signal()
    instanceStatusChanged = Signal(str, object)
    registrationProgressChanged = Signal(str, int)
    registrationCompleted = Signal(str, bool, str)  # (instance_id, success, message)



    def __init__(self, kkt_service: KKTService, tspiot_service: TSPIoTService, cache_ttl_seconds: int = 300, parent=None, is_test=True):
        super().__init__(parent)
        self._service = kkt_service
        self._tspiot_service = tspiot_service
        self.is_test = is_test

        # Менеджер ассинхронных запросов
        self._executor = AsyncExecutor(max_threads=3, parent=self)

        # Менеджер кэша
        self._cache = CacheManager[CashInfo](ttl_seconds=cache_ttl_seconds)
        self._cache_instances = CacheManager[TSPIoTInstancesResponseDTO](ttl_seconds=cache_ttl_seconds)
        self._cache_instance_info = CacheManager[TSPIoTInstanceInfoDTO](ttl_seconds=cache_ttl_seconds)
        self._cache_system_status = CacheManager[TSPIoTSystemsStatusResponseDTO](ttl_seconds=30)


        # Пробрасываем сигналы
        self._executor.loadingChanged.connect(self.loadingChanged)
        self._executor.errorChanged.connect(self.errorChanged)

        # Данные KKT
        self._kkt_list: List[dict] = []
        self._kkt_info_cache: Dict[str, dict] = {}
        self._current_serial: str = ""
        self._current_inn: str = ""

        # Данные TSPIoT
        self._instances_list: List[dict] = []
        self._current_instance_id: str = ""
        self._instances_info_cache: Dict[str, TSPIoTInstanceInfoDTO] = {}
        self._systems_status_cache: Dict[str, TSPIoTSystemsStatusResponseDTO] = {}


    # ─── Public Methods ─────────────────────────────────────────
    def load_kkt(self, reset: bool = False):
        """Асинхронно загружает список касс"""
        if not reset and self._cache.is_valid() and self._kkt_list:
            return

        def on_success(result: CashInfo):
            self._update_cache(result)
            self._cache.set(result)

            if not self._current_serial and self._kkt_list:
                self._current_serial = self._kkt_list[0].get('kktSerial', '')
                self.currentSerialChanged.emit()

            self.kktListChanged.emit()

        def on_error(error_msg: str):
            # Логирование ошибки
            print(f"Error loading KKT: {error_msg}")

        self._executor.execute(
            func=self._service.get_kkt_list,
            on_success=on_success,
            on_error=on_error,
            is_test=self.is_test,
            reset=reset
        )

    def reload_kkt(self):
        """Принудительная перезагрузка"""
        self.load_kkt(reset=True)


    def get_kkt_info(self, serial: str) -> dict:
        """Возвращает информацию о кассе из кэша"""
        return self._kkt_info_cache.get(serial, {})

    def set_current_cash(self, serial: str):
        """Устанавливает текущую кассу"""
        if self._current_serial != serial and serial in self._kkt_info_cache:
            self._current_serial = serial
            self.currentSerialChanged.emit()

    def set_current_inn(self, inn: str):
        self._current_inn = inn

    # ─── Properties ─────────────────────────────────────────────

    @property
    def kktList(self) -> List[dict]:
        return self._kkt_list

    @property
    def currentSerial(self) -> str:
        return self._current_serial

    @property
    def is_loading(self) -> bool:
        return self._executor.is_loading

    @property
    def error(self) -> str:
        return self._executor.error

    @property
    def get_unique_inn(self):
        if not self._kkt_list:
            return []
        return self._service.get_unique_cash_inn()

    # ─── Private Methods ────────────────────────────────────────
    def _update_cache(self, cash_info: CashInfo):
        """Обновляет внутренний кэш из DTO"""
        self._kkt_list.clear()
        self._kkt_info_cache.clear()

        for kkt in cash_info.kkt:
            kkt_dict = self._kkt_to_dict(kkt)
            self._kkt_list.append(kkt_dict)
            self._kkt_info_cache[kkt.kktSerial] = kkt_dict

    def _kkt_to_dict(self, kkt: KktInfo) -> dict:
        return KktMapper.to_dict(kkt)

    # ──────────────────────────────────────────────────────────
    # Новые методы для TSPIoT
    # ──────────────────────────────────────────────────────────

    def reload_instances(self):
        """Принудительная перезагрузка списка инстансов"""
        self.load_instances(reset=True)

    def reload_instance_info(self, instance_id: str):
        """Принудительная перезагрузка информации об инстансе"""
        self.load_instance_info(instance_id, reset=True)

    # def reload_system_status(self, instance_id: str):
    #     """Принудительная перезагрузка статуса систем"""
    #     self.load_system_status(instance_id, reset=True)


    def create_and_register_instance(self, kkt_serial: str, fn_serial: str, kkt_inn: str, is_test=False):
        """
        Асинхронно создаёт и регистрирует инстанс TSPIoT
        """
        def task():
            """Выполнение в отдельном потоке через QRunnable"""
            # Весь цикл создания и регистрации выполняется в сервисе
            result = self._tspiot_service.create_and_registrate_service(
                kkt_serial=kkt_serial,
                fn_serial=fn_serial,
                kkt_inn=kkt_inn,
                is_test=is_test
            )
            return result

        def on_success(result: tuple):
            success, message = result
            self.registrationCompleted.emit(kkt_serial, success, message)
            if success:
                # Обновляем кэш и список
                self.load_instances(reset=True)
                self.load_instance_info(kkt_serial, reset=True)

        def on_error(error_msg: str):
            self.registrationCompleted.emit(kkt_serial, False, error_msg)

        self._executor.execute(
            func=task,
            on_success=on_success,
            on_error=on_error,
            is_test=self.is_test
        )

    def set_current_instance(self, instance_id: str):
        """Устанавливает текущий инстанс"""
        if self._current_instance_id != instance_id:
            self._current_instance_id = instance_id
            self.currentInstanceChanged.emit()
            # Автоматически загружаем информацию
            self.load_instance_info(instance_id)
            # self.load_system_status(instance_id)


    def load_instance_info(self, instance_id: str, reset: bool = False):
        """
        Асинхронно загружает детальную информацию об инстансе
        GET /api/v1/instances/info/{id}
        """
        cache_key = f"instance_info_{instance_id}"

        if not reset and self._cache_instance_info.is_valid(cache_key):
            cached = self._cache_instance_info.get(cache_key)
            if cached:
                logger.debug(f"Используем кэш для инстанса {instance_id}")
                self._instances_info_cache[instance_id] = cached
                self.instanceStatusChanged.emit(instance_id, cached)
                return

        def on_success(result: TSPIoTInstanceInfoDTO):
            self._instances_info_cache[instance_id] = result
            self._cache_instance_info.set(result, key=cache_key)
            self.instanceStatusChanged.emit(instance_id, result)

        def on_error(error_msg: str):
            logger.error(f"Error loading instance info for {instance_id}: {error_msg}")
            self.errorChanged.emit(error_msg)

        self._executor.execute(
            func=self._tspiot_service.get_instance_info,
            on_success=on_success,
            on_error=on_error,
            instance_id=instance_id,
            is_test=self.is_test
        )

    def load_instances(self, reset: bool = False):
        """
        Асинхронно загружает список инстансов TSPIoT
        GET /api/v1/instances/info
        """
        cache_key = "instances_list"

        if not reset and self._cache_instances.is_valid(cache_key) and self._instances_list:
            logger.debug("Используем кэш инстансов")
            return

        def on_success(result: TSPIoTInstancesResponseDTO):
            self._update_instances_cache(result)
            self._cache_instances.set(result, key=cache_key)
            self.instancesListChanged.emit()

            if not self._current_instance_id and self._instances_list:
                self.set_current_instance(self._instances_list[0].get('id', ''))

        def on_error(error_msg: str):
            logger.error(f"Error loading instances: {error_msg}")

        self._executor.execute(
            func=self._tspiot_service.get_instances_info,
            on_success=on_success,
            on_error=on_error,
            is_test=self.is_test,
            reset=reset
        )



    def _update_instances_cache(self, instances_dto: TSPIoTInstancesResponseDTO):
        """Обновляет кэш инстансов"""
        self._instances_list.clear()
        for inst in instances_dto.instances:
            inst_dict = {
                'id': inst.id,
                'port': inst.port,
                'serviceState': inst.serviceState
            }
            self._instances_list.append(inst_dict)

    def clear_tspiot_cache(self):
        """Очищает весь кэш TSPIoT"""
        self._cache_instances.invalidate()
        self._cache_instance_info.invalidate()
        self._cache_system_status.invalidate()
        self._instances_list.clear()
        self._instances_info_cache.clear()
        self._systems_status_cache.clear()
        self._current_instance_id = ""