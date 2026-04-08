from PySide6.QtCore import QObject, Signal, Slot, Property
from old_src.application.application_storage import ApplicationStorage
import logging

logger = logging.getLogger(__name__)


class LMController(QObject):
    """Контроллер для ЛМ ЧЗ - тонкая обертка над ApplicationStorage"""

    lmStatusChanged = Signal()

    def __init__(self, storage: ApplicationStorage, parent=None):
        super().__init__(parent)
        self._storage = storage
        self._storage.lmStatusChanged.connect(self.lmStatusChanged)
        logger.info("✅ LMController инициализирован")

    @Property(str, notify=lmStatusChanged)
    def status(self) -> str:
        return self._storage.lmStatusText

    @Property(str, notify=lmStatusChanged)
    def version(self) -> str:
        return self._storage.lmVersion

    @Property(str, notify=lmStatusChanged)
    def lastSync(self) -> str:
        return self._storage.lmLastConnection

    @Property(str, notify=lmStatusChanged)
    def inn(self) -> str:
        return self._storage.lmInn

    @Property(str, notify=lmStatusChanged)
    def error(self) -> str:
        return self._storage.lmError

    @Property(bool, notify=lmStatusChanged)
    def isConfigured(self) -> bool:
        return self._storage.isLmConfigured

    @Slot(str, int, str, str)
    def saveSettings(self, address: str, port: int, login: str, password: str):
        self._storage.update_lm_settings(address, port, login, password)

    @Slot()
    def refreshInfo(self):
        self._storage.get_application_status()


    @Property(str, notify=lmStatusChanged)
    def ip(self) -> str:
        """IP адрес ЛМ ЧЗ"""
        return self._storage.lmIp

    @Property(str, notify=lmStatusChanged)
    def login(self) -> str:
        """Логин ЛМ ЧЗ"""
        return self._storage.lmLogin

    @Property(int, notify=lmStatusChanged)
    def port(self) -> int:
        """Порт ЛМ ЧЗ"""
        return self._storage.lmPort



class GisMtController(QObject):
    """Контроллер для ГИС МТ - тонкая обертка над ApplicationStorage"""

    gismtStatusChanged = Signal()
    licenseInfoChanged = Signal()

    def __init__(self, storage: ApplicationStorage, parent=None):
        super().__init__(parent)
        self._storage = storage
        self._storage.gismtStatusChanged.connect(self.gismtStatusChanged)
        self._storage.licenseInfoChanged.connect(self.licenseInfoChanged)
        logger.info("✅ GisMtController инициализирован")

    @Property(str, notify=gismtStatusChanged)
    def status(self) -> str:
        return self._storage.gismtStatusText

    @Property(str, notify=gismtStatusChanged)
    def lastConnection(self) -> str:
        return self._storage.gismtLastConnection

    @Property(str, notify=gismtStatusChanged)
    def error(self) -> str:
        return self._storage.gismtError

    @Property(bool, notify=gismtStatusChanged)
    def isConfigured(self) -> bool:
        return self._storage.isGismtConfigured

    @Property(bool, notify=licenseInfoChanged)
    def licenseActive(self) -> bool:
        return self._storage.licenseActive

    @Property(str, notify=licenseInfoChanged)
    def licenseActiveTill(self) -> str:
        return self._storage.licenseActiveTill

    @Property(str, notify=licenseInfoChanged)
    def licenseLastSync(self) -> str:
        return self._storage.licenseLastSync

    @Property(str, notify=licenseInfoChanged)
    def licenseState(self) -> str:
        return self._storage.licenseState

    @Property(str, notify=licenseInfoChanged)
    def licenseVersion(self) -> str:
        return self._storage.licenseVersion

    @Property('QVariant', notify=gismtStatusChanged)
    def settings(self) -> dict:
        return self._storage.gismtSettings

    @Slot(str, bool, bool, str)
    def updateSettings(self, instance_id: str, compatibility_mode: bool,
                       allow_remote: bool, gismt_address: str):
        self._storage.update_gismt_settings(instance_id, compatibility_mode,
                                            allow_remote, gismt_address)

    @Slot()
    def refreshStatus(self):
        self._storage.get_application_status()


class KKTController(QObject):
    """Контроллер для ККТ - тонкая обертка над ApplicationStorage"""

    # Сигналы
    kktListChanged = Signal()
    selectedKktChanged = Signal()
    registrationResultChanged = Signal(dict)
    kktInfoChanged = Signal(dict)
    registrationStatusChanged = Signal()  # Добавлен отсутствующий сигнал

    def __init__(self, storage: ApplicationStorage, parent=None):
        super().__init__(parent)
        self._storage = storage

        # Подключаем сигналы хранилища
        self._storage.kktListChanged.connect(self.kktListChanged)
        self._storage.currentKktChanged.connect(self.selectedKktChanged)
        self._storage.kktInfoUpdated.connect(self.kktInfoChanged)
        self._storage.registrationStatusChanged.connect(self._on_registration_status_changed)

        logger.info("✅ KKTController инициализирован")

    # ==================== Свойства ====================

    @Property(list, notify=kktListChanged)
    def kktList(self) -> list:
        """Список доступных ККТ"""
        return self._storage.kktList

    @Property(str, notify=selectedKktChanged)
    def selectedKkt(self) -> str:
        """Текущий выбранный ККТ"""
        return self._storage.currentKkt

    @Property('QVariant', notify=kktInfoChanged)
    def kktInfo(self) -> dict:
        """Информация о текущем ККТ"""
        return self._storage.get_current_kkt_info()

    @Property(bool, notify=registrationStatusChanged)  # Используем правильный сигнал
    def canRegister(self) -> bool:
        """Можно ли регистрировать выбранную кассу"""
        if not self._storage.currentKkt:
            logger.debug(f"❌ Нельзя регистрировать: нет выбранной кассы")
            return False

        # Получаем актуальный статус из хранилища
        is_registered = self._storage.check_kkt_registration(self._storage.currentKkt)
        can_register = not is_registered

        logger.debug(f"📊 canRegister для {self._storage.currentKkt}: {can_register} (registered={is_registered})")
        return can_register

    @Property(bool, notify=kktListChanged)
    def hasKkt(self) -> bool:
        """Есть ли доступные ККТ"""
        return len(self._storage.kktList) > 0

    # ==================== Слоты ====================

    @Slot(str)
    def selectKkt(self, kkt_serial: str):
        """Выбирает ККТ по серийному номеру"""
        self._storage.set_current_kkt(kkt_serial)

    @Slot()
    def refreshList(self):
        """Обновляет список ККТ"""
        self._storage.refresh_kkt_list()

    @Slot()
    def registerCurrentKkt(self):
        """Регистрирует текущую выбранную кассу"""
        if not self._storage.currentKkt:
            self.registrationResultChanged.emit({
                'success': False,
                'message': 'Не выбрана касса для регистрации'
            })
            return

        kkt_info = self._storage.get_current_kkt_info()

        if not kkt_info:
            self.registrationResultChanged.emit({
                'success': False,
                'message': 'Не удалось получить информацию о кассе'
            })
            return

        result = self._storage.register_kkt(
            kkt_serial=str(self._storage.currentKkt),
            fn_serial=kkt_info.get('fnSerial', ''),
            kkt_inn=kkt_info.get('kktInn', '')
        )
        self.registrationResultChanged.emit(result)

    @Slot(str, str, str, result=dict)
    def registerKkt(self, kkt_serial: str, fn_serial: str, kkt_inn: str) -> dict:
        """Регистрирует ККТ с указанными параметрами"""
        result = self._storage.register_kkt(kkt_serial, fn_serial, kkt_inn)
        self.registrationResultChanged.emit(result)
        return result

    # ==================== Обработчики ====================

    def _on_registration_status_changed(self, kkt_serial: str, is_registered: bool):
        """Обработчик изменения статуса регистрации из хранилища"""
        if kkt_serial == self._storage.currentKkt:
            logger.info(f"📊 Обновлен статус регистрации для {kkt_serial}: {is_registered}")
            self.registrationStatusChanged.emit()  # Уведомляем QML об изменении