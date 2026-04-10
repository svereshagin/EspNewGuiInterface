import logging
import time
from typing import Any, Optional

from dto.tspiot import TspiotCreateInstanceResult, TSPIoTRegistrationServiceResult
from src.dto.tspiot import TSPIoTRequestRegistration, TSPIoTRequestCreateInstance, TspiotCreateInstanceResult, \
    TSPIoTRegistrationResponse, TSPIoTInstancesResponseDTO, TSPIoTInstanceDTO, TSPIoTInstanceInfoDTO, TSPIoTLicenseInfo, \
    TSPIoTRegistrationData
from src.network.tspiot import TSPIoTNetwork

logger =  logging.getLogger(__name__)



class TSPIoTService:
    """
    Сервис для работы с программным модулем ESM
    """

    def __init__(self):
        self.tspiot_agent = TSPIoTNetwork()
        ...

    def create_and_registrate_service(self, kkt_serial, fn_serial, kkt_inn, is_test=False):
        """
        Основная функция для регистрация ТСПиОТ
        1. проверить что такого инстанса ещё нет
        2. создаёт сервис
        3. проверить что создан и не зареган(обход случая долгой реги)
        4. попытаться зарегать
        5. проверить статус регистрации
        """
        reg_dto = TSPIoTRegistrationServiceResult()
        if is_test:
            logger.info("Тестовый режим")
            reg_dto.is_registered = True
            return reg_dto

        else:
            while reg_dto.counter < 3 or reg_dto:

                service_result = self.get_instance_info(kkt_serial)
                logger.info(service_result)

                if service_result is not None and service_result.is_registered:
                    logger.warning("Сервис уже зарегестрирован")
                    reg_dto.message = "Сервис уже зарегестрирован"
                    reg_dto.is_registered = True
                    break

                elif service_result == 204 or not service_result.is_registered:
                    logger.info(f"Получен ответ от оркестратора 204 - сервис ещё не создан\nПопытка создания сервиса {reg_dto.counter}")
                    create_esm_service_result = self.create_esm_instance(kkt_serial)

                    if create_esm_service_result.success:
                        logger.info(f"Успешно создали инстанс ESM\nПопытка провести регистрации сервиса номер {reg_dto.counter}")
                    elif not create_esm_service_result.success and create_esm_service_result.status == "Уже существует":
                        logger.info(f"Получили 1010, инстанс создан но не зарегестрирован.\nПопытка провести регистрацию сервиса  {reg_dto.counter}")

                    start_time = time.time()
                    self.register_tspiot(kkt_serial,kkt_serial,fn_serial, kkt_inn)
                    end_time = time.time()
                    logger.info(f"⏱️ регистрация выполнена за {end_time - start_time:.4f} секунд")
                elif service_result is None:
                    reg_dto.counter+=1
        return reg_dto

    def get_instance_info(self, kkt_serial, is_test=False):
        """
        Полная информация о сервисе ESM
        """
        if is_test:
            return TSPIoTInstanceInfoDTO(logPath='C:\\ProgramData\\esp\\esm\\um\\log', state='Зарегистрирован', clientPort=51401, version='1.6.1.0', licenses=[TSPIoTLicenseInfo(isActive=True, activeTill='2026-05-10 00:00:00', lastSync='2026-04-10 15:28:09')], regData=TSPIoTRegistrationData(tspiotId='469010be-3b89-4983-bc13-fd125bcf5a3f', gismtTspiotId='2cb9ba1d-a893-438e-b6c5-593db95ab641', kktSerial='00106327428745', fnSerial='9999078902018941', kktInn='9717169631', espToken='eyJ0eXAiOiJKV1QiLCJraWQiOiJLLTFhZWlnOTI1IiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiIwMDAwMDAwMDAxMDQwMDE0IiwianRpIjoiOGI0YmI3YjgtZDYwNS00N2I4LWIwMTItNjE5MmI2MDlkZjUyIiwiYXVkIjpbIkNBU0hERVNLX1NUQVRTIl0sImNpZCI6MjQzLCJybm0iOiIwMDAwMDAwMDAxMDQwMDE0Iiwiem5pZCI6IjAwMTA2MzI3NDI4NzQ1IiwiZm5pZCI6Ijk5OTkwNzg5MDIwMTg5NDEiLCJpbm4iOiI5NzE3MTY5NjMxIiwiY3RwIjoiTUdNIiwibmJmIjoxNzc1ODI0NTEzLCJleHAiOjE3NzcwMzQxNzN9.GruGqyfcy6gR3eXp-yARd3etIvM4zqNznFpTJrGZvzcV4jgucm-5p56KBgZslW4VwE9VH4DECbUsUyQjv94jse34SMWSu5bNrh01wmV2sLN8HIDpioZ69wA1CNILmx6bZsBU4ftfgCrrj7R3aWdWTslgMN4DlhLxuEdtSY71_7nbinOwp5Q7A7AkWg7m-rrI3rAqb09cWE5DhZnPEhBhlYlHWWxKnh9XEqeE9VCz1SznoZI1TnSKaGlc9NgL1EKSgNc7OsA1WKDYoBJHJ8Efgx82pu9ag6qUuj9nA7ddj6EscbZKkLO8TE0w-hM6xPamtouszMifzm72Vm6NoRUK8g'))
        else:
            return self.tspiot_agent.get_instance_info(kkt_serial)


    def get_instances_info(self, is_test=False):
        if is_test:
            instances: TSPIoTInstancesResponseDTO = TSPIoTInstancesResponseDTO(instances=[TSPIoTInstanceDTO(id='00106327428745', port=50401, serviceState='Работает')])
            return instances
        else:
            instances_info = self.tspiot_agent.get_instances_info()



    def register_tspiot(self, service_id, kkt_serial, fn_serial, kkt_inn, is_test=False):
        dto = TSPIoTRequestRegistration(service_id, kkt_serial, fn_serial, kkt_inn)
        if is_test:
            return TSPIoTRegistrationResponse(success=True, tspiot_id='469010be-3b89-4983-bc13-fd125bcf5a3f', status=None, error_message=None)
        else:
            register_result = self.tspiot_agent.register_tspiot(dto)
            if register_result.success:
                logger.info("Регистрация прошла успешно")
            else:
                logger.info("Регистрация прошла с ошибкой")
            return register_result

    def create_esm_instance(self, kkt_serial: str, is_test=False) -> Optional[TspiotCreateInstanceResult]:
        dto = TSPIoTRequestCreateInstance(kkt_serial=kkt_serial)
        if is_test:
            result = TspiotCreateInstanceResult(success=True, tspiot_id='00106327428745', status='Создан', error_message=None, error_code=None)
            return result
        else:
            create_esm_service_result = self.tspiot_agent.create_esm_service(dto)
            return create_esm_service_result


