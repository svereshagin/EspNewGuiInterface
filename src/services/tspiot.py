import logging

from src.dto.tspiot import TSPIoTRequestRegistration, TSPIoTRequestCreateInstance
from src.network.tspiot import TSPIoTNetwork

logger =  logging.getLogger(__name__)


class TSPIoTService:
    """
    Сервис для работы с программным модулем ESM
    """

    def __init__(self):
        self.tspiot_agent = TSPIoTNetwork()
        ...

    def get_instance_info(self):
        ...

    def register_tspiot(self, id, kktSerial, fnSerial, kktInn, is_test=False):
        dto = TSPIoTRequestRegistration(id, kktSerial, fnSerial, kktInn)
        register_result = self.tspiot_agent.register_tspiot(dto)
        ...

    def create_esm_instance(self, kkt_setial: str):
        dto = TSPIoTRequestCreateInstance(kkt_serial=kkt_setial)
        create_esm_service_result = self.tspiot_agent.create_esm_service(dto)

