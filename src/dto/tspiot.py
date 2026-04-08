from dataclasses import dataclass



@dataclass
class ESM:
    #url 1.2.3 -> 'http://127.0.0.1:51077/api/v1/instances/info/0128245621'

    logPath: str #путь к логам
    state: str
    clientPort: int
    version: str
    licenses: list[str]
    isActive: bool
    activeTill: str
    lastSync: str
    regData: str #пока неизвестно что там придёт
    tspiotId: str
    gismtTspiotId: str
    kktSerial: str
    fnSerial: str
    kktInn: str
    espToken: str