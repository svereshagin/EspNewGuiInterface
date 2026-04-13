# Данный модуль отвечает за следующие вещи
# 1. получить состояние инстанса ESM
# 2. создать службу esm
# 3. зарегистрировать её
#
#

import logging
import sys
from typing import Optional

import httpx

from dto.tspiot import TSPIoTRequestCreateInstance, TspiotCreateInstanceResult, TSPIoTRequestRegistration, \
    TSPIoTRegistrationResponse, TSPIoTInstancesResponseDTO, ServiceState, TSPIoTInstanceDTO, TSPIoTRegistrationData, \
    TSPIoTInstanceInfoDTO, TSPIoTLicenseInfo
from enums.network_errors.tspiot import TspiotResponseMessages
from network.base import ApiClient

logging.basicConfig(
    level=logging.DEBUG,                     # можно INFO, если не нужны DEBUG
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)




class TSPIoTNetwork(ApiClient):
    """
    Класс для создания и регистрации инстанса  TSPIOT.qml

    - создание инстанса ESM
    - регистрация TSPIoT
    - получение информации об инстансах
    - получение статусов систем

    """
    ENDPOINT = "/api/v1/TSPIOT.qml"
    ESM_INFO_ENDPOINT = "/api/v1/instances/info"
    ESM_STATUS_ENDPOINT = "/api/v1/status/"

    def create_esm_service(self, data: TSPIoTRequestCreateInstance):
        """Запрос на добавление сервиса ЕСМ /api/v1/TSPIOT.qml (POST)"""
        logger.debug("Создание ESM сервиса для kkt_serial=%s", data.kkt_serial)

        try:
            response = self.post(self.ENDPOINT, data={"id": data.kkt_serial})
            return self._process_create_response(response, data.kkt_serial)
        except httpx.TimeoutException:
            return self._create_error_result(TspiotResponseMessages.TIMEOUT_ERROR.value)
        except httpx.ConnectError:
            return self._create_error_result(TspiotResponseMessages.CONNECTION_ERROR.value)
        except Exception as e:
            return self._create_error_result(f"{TspiotResponseMessages.CRITICAL_ERROR_PREFIX.value}{e}")

    def register_tspiot(self, data: TSPIoTRequestRegistration) -> TSPIoTRegistrationResponse:
        """
        Регистрирует TSPIOT
        PUT -> "/api/v1/TSPIOT.qml"
        """
        logger.debug("Регистрация TSPIOT для kktSerial=%s", data.kktSerial)
        payload = {
            "id": data.id,
            "kktSerial": data.kktSerial,
            "fnSerial": data.fnSerial,
            "kktInn": data.kktInn
        }
        try:
            response = self.put(self.ENDPOINT, data=payload, timeout=120)
            logger.debug("PUT %s → статус %d", self.ENDPOINT, response.status_code)

            # Успешная регистрация (201 Created)
            if response.status_code == 201:
                response_data = response.json() if response.text else {}
                tspiot_id = response_data.get("tspiotId") or response_data.get("id")
                logger.info("TSPIOT зарегистрирован: %s", tspiot_id)
                return TSPIoTRegistrationResponse(
                    success=True,
                    tspiot_id=tspiot_id,
                    error_message=None
                )

            # Обработка ошибки 400
            if response.status_code == 400:
                return self._handle_400_registration(response, data.kktSerial)

            # Обработка остальных статусов
            return self._handle_other_registration_status(response)

        except httpx.TimeoutException:
            logger.error(TspiotResponseMessages.TIMEOUT_ERROR.value)
            return TSPIoTRegistrationResponse(
                success=False,
                tspiot_id=None,
                error_message=TspiotResponseMessages.TIMEOUT_ERROR.value
            )
        except httpx.ConnectError:
            logger.error(TspiotResponseMessages.CONNECTION_ERROR.value)
            return TSPIoTRegistrationResponse(
                success=False,
                tspiot_id=None,
                error_message=TspiotResponseMessages.CONNECTION_ERROR.value
            )
        except Exception as e:
            logger.error(f"Ошибка регистрации: {e}")
            return TSPIoTRegistrationResponse(
                success=False,
                tspiot_id=None,
                error_message=str(e)
            )

    def get_instances_info(self) -> Optional[TSPIoTInstancesResponseDTO]:
        """
        1.2.2. Запрос получения списка запущенных ЕСМ
        GET /api/v1/instances/info

        Returns:
            TSPIoTInstancesResponseDTO - объект со списком инстансов
            None - если произошла ошибка или нет данных
        """
        logger.debug("Запрос списка инстансов ЕСМ: %s", self.ESM_INFO_ENDPOINT)

        try:
            response = self.get(self.ESM_INFO_ENDPOINT)
            logger.debug("GET %s → статус %d", self.ESM_INFO_ENDPOINT, response.status_code)

            if response.status_code == 200:
                data = response.json()
                instances_list = []

                for inst_data in data.get("instances", []):
                    instance = TSPIoTInstanceDTO(
                        id=inst_data.get("id", ""),
                        port=inst_data.get("port", 0),
                        serviceState=inst_data.get("serviceState", ServiceState.UNKNOWN)
                    )
                    instances_list.append(instance)

                result = TSPIoTInstancesResponseDTO(instances=instances_list)
                logger.info("Найдено инстансов ЕСМ: %d", result.count)
                for inst in instances_list:
                    logger.debug("  - ID: %s, порт: %d, состояние: %s", inst.id, inst.port, inst.serviceState)

                return result

            elif response.status_code == 204:
                # Нет ни одного инстанса ESM, ответ пустой
                logger.info("Нет зарегистрированных инстансов ЕСМ (204)")
                return TSPIoTInstancesResponseDTO(instances=[])

            else:
                logger.error("Ошибка получения списка инстансов: статус %d", response.status_code)
                return None
        except Exception as e:
            logger.error(e)

    def get_instance_info(self, instance_id: str) -> None | TSPIoTInstanceInfoDTO | int:
        """
        1.2.3. Запрос получения информации из ЕСМ
        GET /api/v1/instances/info/{id}

        Returns:
            TSPIoTInstanceInfoDTO - детальная информация об инстансе
            None - если произошла ошибка или инстанс не найден
        """
        endpoint_path = self.ESM_INFO_ENDPOINT + "/"
        logger.debug("Запрос информации об инстансе: %s%s", endpoint_path, instance_id)

        try:
            response = self.get(f'{endpoint_path}{instance_id}')
            logger.debug("GET %s%s → статус %d", endpoint_path, instance_id, response.status_code)

            if response.status_code == 200:
                data = response.json()
                logger.info("Получена информация об инстансе %s", instance_id)
                return self._parse_instance_info_response(data)

            elif response.status_code == 204:
                logger.warning("Нет информации об инстансе %s (204)", instance_id)
                return 204

        except httpx.TimeoutException:
            logger.error(TspiotResponseMessages.TIMEOUT_ERROR.value)
            return None
        except httpx.ConnectError:
            logger.error(TspiotResponseMessages.CONNECTION_ERROR.value)
            return None
        except Exception as e:
            logger.exception("Ошибка при получении информации об инстансе %s: %s", instance_id, e)
            return None

    def _parse_instance_info_response(self, data: dict) -> TSPIoTInstanceInfoDTO:
        """Парсит JSON ответ в TSPIoTInstanceInfoDTO"""

        # Парсим лицензии (может быть несколько)
        licenses_list = []
        for lic in data.get("licenses", []):
            license_info = TSPIoTLicenseInfo(
                isActive=lic.get("isActive", False),
                activeTill=lic.get("activeTill", ""),
                lastSync=lic.get("lastSync", "")
            )
            licenses_list.append(license_info)

        # Парсим регистрационные данные
        reg_data_raw = data.get("regData", {})
        registration_data = TSPIoTRegistrationData(
            tspiotId=reg_data_raw.get("tspiotId", ""),
            gismtTspiotId=reg_data_raw.get("gismtTspiotId", ""),
            kktSerial=reg_data_raw.get("kktSerial", ""),
            fnSerial=reg_data_raw.get("fnSerial", ""),
            kktInn=reg_data_raw.get("kktInn", ""),
            espToken=reg_data_raw.get("espToken", "")
        )

        # Создаем и возвращаем DTO
        return TSPIoTInstanceInfoDTO(
            logPath=data.get("logPath", ""),
            state=data.get("state", ""),
            clientPort=data.get("clientPort", 0),
            version=data.get("version", ""),
            licenses=licenses_list,
            regData=registration_data
        )


    def _process_create_response(self, response, kkt_serial: str):
        """Обработка ответа в зависимости от статуса"""
        handlers = {
            201: self._handle_201_create,
            400: self._handle_400_create,
        }

        handler = handlers.get(response.status_code, self._handle_other_create_status)
        return handler(response, kkt_serial)


    def _handle_201_create(self, response, kkt_serial: str):
        """Обработка успешного создания (201)"""
        response_data = response.json() if response.text else {}

        if response_data.get("id"):
            result = TspiotCreateInstanceResult(
                success=True,
                tspiot_id=response_data["id"],
                status="Создан"
            )
            logger.info("ESM сервис создан: %s", result.tspiot_id)
            return result

        return self._create_error_result("Не получен id в ответе")

    def _handle_400_create(self, response, kkt_serial: str):
        """Обработка ошибки 400"""
        response_data = response.json() if response.text else {}
        error = response_data.get('error', {})
        error_code = error.get('code')
        error_text = error.get('text', '')

        # Уже существует - не критично
        if error_code == 1010 or "уже существует" in error_text:
            logger.warning("ESM сервис уже существует: %s", kkt_serial)
            return TspiotCreateInstanceResult(
                success=False,
                tspiot_id=kkt_serial,
                status="Уже существует",
                error_message=error_text,
            )

        return self._create_error_result(error_text or f"Ошибка 400: {response_data}")

    def _handle_other_create_status(self, response):
        """Обработка остальных статусов"""
        response_data = response.json() if response.text else {}
        error_msg = response_data.get('text', f"Ошибка {response.status_code}")
        return self._create_error_result(error_msg)

    def _create_error_result(self, error_message: str):
        """Создание результата с ошибкой"""
        result = TspiotCreateInstanceResult(success=False, error_message=error_message)
        logger.error(error_message)
        return result

    def _handle_other_registration_status(self, response) -> TSPIoTRegistrationResponse:
        """Обработка остальных статусов при регистрации"""
        response_data = response.json() if response.text else None
        logger.warning("Неожиданный статус %s", response.status_code)

        error_msg = response_data.get('text',
                                      f"Сервер вернул {response.status_code}") if response_data else f"Сервер вернул {response.status_code}"

        return TSPIoTRegistrationResponse(
            success=False,
            tspiot_id=None,
            error_message=error_msg
        )

    def is_tspiot_empty(self, tspiot_id: str) -> bool:
        return len(tspiot_id) > 1 if tspiot_id else False











