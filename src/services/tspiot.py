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

    def register_tspiot(self, id, kkt_serial, fn_serial, kkt_inn, is_test=False):
        dto = TSPIoTRequestRegistration(id, kkt_serial, fn_serial, kkt_inn)
        if is_test:
            ...
        else:
            register_result = self.tspiot_agent.register_tspiot(dto)

    def create_esm_instance(self, kkt_serial: str, is_test=False):
        dto = TSPIoTRequestCreateInstance(kkt_serial=kkt_serial)
        if is_test:
            ...
        else:
            create_esm_service_result = self.tspiot_agent.create_esm_service(dto)

    def get_instance_info(self, kkt_serial, is_test=False):
        if is_test:
            ...
        else:
            get_instance_result = self.tspiot_agent.get_instance_info(kkt_serial)