#===============================================================
# Данный модель отвечает за работу с ККТ в качестве контроллера данных (Py -> QT) уже полученны данных
# Технический спектр выполняющийся здесь:
#           1. Отображение информации о ККТ
#           2. Выбор компании из списка компаний через ИНН
#           3. Обновление списка ККТ(авто/через кнопку)
#           4. Отображение статуса регистрации
#           5. Изменение информации о конкретном экземпляре ККТ
#           6.
#===============================================================


import logging

from PySide6.QtCore import Signal, QObject, Property, Slot

from src.application.application_storage import ApplicationStorage

logger = logging.getLogger(__name__)






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
        self._current_inn: None | str = None
        # Подключаем сигналы хранилища
        self._storage.kktListChanged.connect(self.kktListChanged)
        self._storage.currentKktChanged.connect(self.selectedKktChanged)
        self._storage.kktInfoUpdated.connect(self.kktInfoChanged)
        self._storage.registrationStatusChanged.connect(self._on_registration_status_changed)
        logger.info("KKTController инициализирован")

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