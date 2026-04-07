import logging
from typing import Optional

from PySide6.QtCore import Signal, QObject, Property

from src.domain.controlmodule.entity import ControlModuleInfo

logger = logging.getLogger(__name__)


class ControlModuleViewModel(QObject):
    """ViewModel для отображения данных ControlModule"""

    dataChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._data = ControlModuleInfo(app_path="/app/path", version='version',
                                       log_path="/logs/path2")


    @Property(str, notify=dataChanged)
    def appPath(self) -> str:
        return self._data.app_path

    @Property(str, notify=dataChanged)
    def version(self) -> str:
        return self._data.version

    @Property(str, notify=dataChanged)
    def logPath(self) -> str:
        return self._data.log_path

    @Property(bool, notify=dataChanged)
    def hasData(self) -> bool:
        """Проверка, есть ли данные"""
        return not self._data.is_empty()

    def update(self, info: Optional['ControlModuleInfo']):
        """Обновляет ViewModel из DTO"""
        if info and isinstance(info, ControlModuleInfo):
            self._data = ControlModuleInfo(
                app_path=info.app_path,
                version=info.version,
                log_path=info.log_path
            )
        else:
            logger.info(f'Вернулось пустое: {info}')
            self._data = ControlModuleInfo()

        self.dataChanged.emit()