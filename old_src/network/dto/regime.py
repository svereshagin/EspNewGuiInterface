from dataclasses import dataclass
from typing import List, Optional
from enum import Enum


class DatabaseStatus(Enum):
    """Статус базы данных ЛМ ЧЗ"""
    READY = "READY"
    UNREGISTERED = "UNREGISTERED"
    ERROR = "ERROR"


@dataclass
class LicenseInfo:
    """Информация о лицензии"""
    licenses: List[dict]  # информация о лицензии (массив объектов)
    isActive: bool  # активна лицензия или нет
    activeTill: str  # срок действия лицензии (дата формата Go)
    lastSync: str  # время последней проверки лицензии (дата формата Go)


@dataclass
class RegistrationData:
    """Регистрационные данные"""
    tspiotId: str  # идентификатор ТС ПИоТ
    gismtTspiotId: str  # идентификатор в ГИС МТ
    kktSerial: str  # серийный номер кассы
    fnSerial: str  # серийный номер ФН
    kktInn: str  # ИНН на который зарегистрирована касса
    espToken: str  # токен в системе ЕСП


@dataclass
class OsInfo:
    """Информация об операционной системе контролера ЛМ ЧЗ"""
    OsType: str  # тип ОС (linux/windows)
    OsVersion: str  # версия ОС
    OsArch: str  # архитектура ОС


@dataclass
class BlockedCisInfo:
    """Информация о заблокированных КМ"""
    localDocCount: int  # количество заблокированных КМ в локальной БД ЛМ ЧЗ
    serverDocCount: int  # количество заблокированных КМ в списке сервера ЛМ ЧЗ


@dataclass
class BlockedGtinInfo:
    """Информация о заблокированных GTIN"""
    localDocCount: int  # количество заблокированных gtin в локальной БД ЛМ ЧЗ
    serverDocCount: int  # количество заблокированных gtin в списке сервера ЛМ ЧЗ


@dataclass
class LmStatusInfo:
    """Информация о статусе ЛМ ЧЗ"""
    dbVersion: str  # версия базы ЛМ ЧЗ
    inn: str  # ИНН на который зарегистрирован ЛМ ЧЗ
    inst: str  # ID инстанса ЛМ ЧЗ
    isGreyGtin: bool  # признак работы с серыми gtin
    lastSync: int  # время последней синхронизации БД ЛМ ЧЗ (timestamp)
    lastUpdate: int  # время последнего обновления ЛМ ЧЗ (timestamp)
    name: str  # наименование ЛМ ЧЗ
    operationMode: str  # статус ЛМ ЧЗ
    replicationStatus: Optional[dict]  # информация о репликации БД ЛМ ЧЗ
    blocked_cis: BlockedCisInfo  # информация о заблокированных КМ
    blocked_gtin: BlockedGtinInfo  # информация о заблокированных GTIN
    requiresDownload: bool  # требуется или нет загрузка БД ЛМ ЧЗ
    serviceUrl: str  # URL сервиса обновлений БД ЛМ ЧЗ
    status: DatabaseStatus  # статус БД ЛМ ЧЗ
    version: str  # версия ЛМ ЧЗ


@dataclass
class Controlmodule_instance_info_DTO:
    """DTO для информации о состоянии контрольного модуля"""
    # Основная информация
    logPath: str  # путь к лог файлам
    state: str  # статус регистрации
    clientPort: int  # порт для подключения ПМСР (сервис проверки КМ)
    version: str  # версия ЕСМ

    # Информация о лицензии
    licenseInfo: LicenseInfo  # информация о лицензии

    # Регистрационные данные
    regData: RegistrationData  # регистрационные данные

    # Информация о контролере ЛМ ЧЗ
    controllerVersion: str  # версия контролера ЛМ ЧЗ
    code: int  # статус работы ЛМ ЧЗ (0 - Ок, 1 - Ошибка)
    osInfo: OsInfo  # информация об операционной системе контролера ЛМ ЧЗ
    lmStatus: LmStatusInfo  # информация о статусе ЛМ ЧЗ