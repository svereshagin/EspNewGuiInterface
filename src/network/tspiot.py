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
    TSPIoTRegistrationResponse
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
    Класс для создания и регистрации инстанса  tspiot
    """
    ENDPOINT = "/api/v1/tspiot"
    ESM_INFO_ENDPOINT = "/api/v1/instances/info/"

    def create_esm_service(self, data: TSPIoTRequestCreateInstance):
        """Запрос на добавление сервиса ЕСМ /api/v1/tspiot (POST)"""
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
        PUT -> "/api/v1/tspiot"
        """
        logger.debug("Регистрация TSPIOT для kktSerial=%s", data.kktSerial)
        payload = {
            "id": data.id,
            "kktSerial": data.kktSerial,
            "fnSerial": data.fnSerial,
            "kktInn": data.kktInn
        }
        try:
            response = self.put(self.ENDPOINT, data=payload)
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


    def get_instance_info(self, kkt_id: str) -> Optional[bool]:
        """Получает информацию об инстансе"""
        logger.debug("Запрос к %s%s", self.ESM_INFO_ENDPOINT, kkt_id)

        try:
            response = self.get(f'{self.ESM_INFO_ENDPOINT}{kkt_id}')

            if response.status_code == 200:
                data = response.json()
                result = self.is_tspiot_empty(data.get("regData", {}).get("tspiotId", ""))
                logger.debug("Инстанс %s существует: %s", kkt_id, result)
                return result

            logger.warning("Статус %s при проверке инстанса %s", response.status_code, kkt_id)

        except httpx.TimeoutException:
            logger.error(TspiotResponseMessages.TIMEOUT_ERROR.value)
            return None
        except httpx.ConnectError:
            logger.error(TspiotResponseMessages.CONNECTION_ERROR.value)
            return None
        except Exception as e:
            logger.exception("Ошибка при проверке инстанса %s: %s", kkt_id, e)
            return None



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








# Реальные данные из CashInfo
KKT_SERIAL = "00106327428745"
FN_SERIAL = "9999078902018941"
KKT_INN = "9717169631"
KKT_RNM = "0000000001040014"
MODEL_NAME = "АТОЛ FPrint-22ПТК"
DKKT_VERSION = "10.10.8.23"




def main():
    logger.info("=" * 70)
    logger.info("Тестирование TSPIoTNetwork с реальными данными кассы")
    logger.info("=" * 70)
    logger.info(f"Касса: {KKT_SERIAL}")
    logger.info(f"ФН: {FN_SERIAL}")
    logger.info(f"ИНН: {KKT_INN}")
    logger.info(f"Модель: {MODEL_NAME}")
    logger.info(f"Версия ДККТ: {DKKT_VERSION}")
    logger.info("=" * 70)

    # Создаём клиент
    with TSPIoTNetwork() as network:
        # Проверяем конфигурацию
        # Шаг 1: Проверить, существует ли уже инстанс
        logger.info("\n1️⃣ Проверка существования инстанса...")
        exists = network.get_instance_info(KKT_SERIAL)
        logger.info(f"   Инстанс существует: {exists}")

        # Шаг 2: Создать ESM сервис (если не существует)
        logger.info("\n2️⃣ Создание ESM сервиса...")
        create_request = TSPIoTRequestCreateInstance(kkt_serial=KKT_SERIAL)
        create_result = network.create_esm_service(create_request)

        logger.info(f"   Success: {create_result.success}")
        logger.info(f"   Status: {create_result.status}")
        logger.info(f"   tspiot_id: {create_result.tspiot_id}")
        if create_result.error_message:
            logger.info(f"   Error: {create_result.error_message}")
        if create_result.error_code:
            logger.info(f"   Error code: {create_result.error_code}")

        # Шаг 3: Зарегистрировать TSPIOT
        logger.info("\n3️⃣ Регистрация TSPIOT...")
        register_request = TSPIoTRequestRegistration(
            id=KKT_SERIAL,
            kktSerial=KKT_SERIAL,
            fnSerial=FN_SERIAL,
            kktInn=KKT_INN
        )
        register_result = network.register_tspiot(register_request)

        logger.info(f"   Success: {register_result.success}")
        logger.info(f"   tspiot_id: {register_result.tspiot_id}")
        if register_result.error_message:
            logger.info(f"   Error: {register_result.error_message}")

        # Шаг 4: Повторно проверить статус (опционально)
        logger.info("\n4️⃣ Повторная проверка статуса...")
        exists_after = network.get_instance_info(KKT_SERIAL)
        logger.info(f"   Инстанс существует после операций: {exists_after}")

        logger.info("\n" + "=" * 70)
        logger.info("✅ Тестирование завершено")
        logger.info("=" * 70)


if __name__ == "__main__":
    main()