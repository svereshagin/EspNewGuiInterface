import enum
import logging
from dataclasses import dataclass
from typing import Optional

import httpx

from old_src.core.config import ApiSettings
from old_src.network.base import ApiClient

logger = logging.getLogger(__name__)


class TspiotResponseMessages(enum.Enum):
    """Константы сообщений — удобно для локализации в будущем"""
    TIMEOUT_ERROR = "Превышено время ожидания ответа от оркестратора"
    CONNECTION_ERROR = "Не удалось установить соединение с оркестратором"
    REQUEST_ERROR_PREFIX = "Ошибка выполнения запроса: "
    MISSING_FIELDS = "В ответе отсутствуют поля 'id' и/или 'serviceState'"
    NON_201_RESPONSE = "Сервер вернул код"
    JSON_PARSE_ERROR = "Не удалось разобрать JSON-ответ"
    CRITICAL_ERROR_PREFIX = "Критическая ошибка при создании tspiot: "
    SUCCESS_PREFIX = "tspiot успешно запущен → id="
    UNEXPECTED_STATUS_PREFIX = "Сервис находится в состоянии"


@dataclass
class RequestRegistrationTSPIOT_DTO:
    id: str  # идентификатор инстанса ЕСМ
    kktSerial: str  # Серийный номер кассы
    fnSerial: str  # Серийный номер ФН
    kktInn: str  # ИНН на который зарегистрирована касса


@dataclass
class ResponseRegistrationTSPIOT_DTO:
    tspiotId: str | None
    result: bool = False
    error_msg: Optional[str] = None


@dataclass
class RequestCreateInstanceTSPIOT_DTO:
    kkt_serial: str  # идентификатор инстанса ЕСМ заполняется значением kktSerial из списка ДККТ
    port: int | None = None  # порт для подключения оркестратора
    softPort: int | None = None  # ПОРТ ДЛЯ ПМСР


@dataclass
class TspiotResult:
    """Структура-результат выполнения запроса"""
    success: bool = False
    tspiot_id: Optional[str] = None
    status: Optional[str] = None
    error_message: Optional[str] = None







class TspiotSetup:
    """
    Класс для создания и запуска экземпляра tspiot (аналог RequestSetupEcm из C++)
    """

    ENDPOINT = "/api/v1/tspiot"
    ESM_INFO_ENDPOINT = "/api/v1/instances/info/"

    def __init__(self):
        self._result: TspiotResult = TspiotResult()
        self._config = ApiSettings()
        self._client: Optional[httpx.Client] = None

    def _get_client(self) -> httpx.Client:
        """Создает новый клиент, если его нет или он закрыт"""
        if self._client is None or self._client.is_closed:
            self._client = httpx.Client(
                base_url=self._config.orchestrator_url,
                timeout=80.0
            )
            logger.debug("✅ Создан новый HTTPX клиент для TspiotSetup")
        return self._client

    def _close_client(self):
        """Закрывает клиент"""
        if self._client and not self._client.is_closed:
            self._client.close()
            logger.debug("🔒 Клиент TspiotSetup закрыт")

    def get_instance_info(self, kkt_id):
        try:
            client = self._get_client()
            response = client.get(
                self.ESM_INFO_ENDPOINT+kkt_id,
            )
            if response.status_code == 200:
                data = response.json()
                result = True if len(data["regData"]["tspiotId"]) > 1 else False
                return result
            else:
                logger.info("Status code is not 200")
        except httpx.TimeoutException:
            logger.error(TspiotResponseMessages.TIMEOUT_ERROR.value)
            return None

    def register_tspiot(self, data: RequestRegistrationTSPIOT_DTO) -> ResponseRegistrationTSPIOT_DTO:
        """
        Регистрирует TSPIOT
        PUT -> "/api/v1/tspiot"
        """
        payload = {
            "id": data.id,
            "kktSerial": data.kktSerial,
            "fnSerial": data.fnSerial,
            "kktInn": data.kktInn
        }

        client = self._get_client()

        try:
            response = client.put(
                self.ENDPOINT,
                json=payload
            )
            logger.debug(f"PUT {self.ENDPOINT} → статус {response.status_code}")

            # Пытаемся получить тело ответа
            response_data = response.json() if response.text else None

            # Успешная регистрация (201 Created)
            if response.status_code == 201 and response_data:
                tspiot_id = response_data.get("tspiotId") or response_data.get("id")
                logger.info(f"Network: TSPIOT зарегистрирован: {tspiot_id}")
                return ResponseRegistrationTSPIOT_DTO(
                    result=True,
                    tspiotId=tspiot_id,
                    error_msg=None
                )

            # Обработка ошибки 400 (Bad Request)
            if response.status_code == 400 and response_data:
                error = response_data.get('error', {})
                error_code = error.get('code')
                error_text = error.get('text', '')
                error_description = error.get('description', '')

                logger.warning(f"⚠️ Ошибка 400: code={error_code}, text={error_text}")

                # Служба уже зарегистрирована
                if error_code == 1011 or "уже зарегистрирована" in error_text:
                    logger.info(f"TSPIOT для {data.kktSerial} уже зарегистрирован")
                    return ResponseRegistrationTSPIOT_DTO(
                        result=True,
                        tspiotId=data.id,
                        error_msg=None
                    )

                # Другая ошибка
                error_msg = f"{error_text}: {error_description}" if error_description else error_text
                return ResponseRegistrationTSPIOT_DTO(
                    result=False,
                    tspiotId=None,
                    error_msg=error_msg
                )

            # Обработка других кодов ответа
            logger.warning(f"Неожиданный статус {response.status_code}")
            error_msg = response_data.get('text',
                                          f"Сервер вернул {response.status_code}") if response_data else f"Сервер вернул {response.status_code}"
            return ResponseRegistrationTSPIOT_DTO(
                result=False,
                tspiotId=None,
                error_msg=error_msg
            )

        except httpx.TimeoutException:
            logger.error(TspiotResponseMessages.TIMEOUT_ERROR.value)
            return ResponseRegistrationTSPIOT_DTO(
                result=False,
                tspiotId=None,
                error_msg=TspiotResponseMessages.TIMEOUT_ERROR.value
            )

        except httpx.ConnectError:
            logger.error(TspiotResponseMessages.CONNECTION_ERROR.value)
            return ResponseRegistrationTSPIOT_DTO(
                result=False,
                tspiotId=None,
                error_msg=TspiotResponseMessages.CONNECTION_ERROR.value
            )

        except Exception as e:
            logger.error(f"Ошибка регистрации: {e}")
            return ResponseRegistrationTSPIOT_DTO(
                result=False,
                tspiotId=None,
                error_msg=str(e)
            )


    def create_esm_service(self, data: RequestCreateInstanceTSPIOT_DTO) -> TspiotResult:
        """1.2.6. Запрос на добавление сервиса ЕСМ /api/v1/tspiot"""
        self._result = TspiotResult()
        payload = {"id": data.kkt_serial}

        try:
            response = self._get_client().post(self.ENDPOINT, json=payload)
            logger.debug(f"POST {self.ENDPOINT} → статус {response.status_code}")

            response_data = response.json() if response.text else None

            if response.status_code == 201 and response_data and response_data.get('id'):
                self._result.success = True
                self._result.tspiot_id = response_data['id']
                self._result.status = "Создан"
                return self._result

            if response.status_code == 400 and response_data:
                error = response_data.get('error', {})
                error_code = error.get('code')
                error_text = error.get('text', '')

                if error_code == 1010 or "уже существует" in error_text:
                    self._result.success = False
                    self._result.tspiot_id = data.kkt_serial
                    self._result.status = "Уже существует"
                    self._result.error_message = error_text
                    self._result.error_code = error_code
                    return self._result
            if response.status_code == 500:
                #На даный момент считаем, что это ошибка означает, что уже есть инстанс esm

                pass
            self._result.success = False
            self._result.error_message = response_data.get('text',
                                                           f"Ошибка {response.status_code}") if response_data else f"Ошибка {response.status_code}"
            return self._result

        except httpx.TimeoutException:
            self._result.error_message = TspiotResponseMessages.TIMEOUT_ERROR.value
        except httpx.ConnectError:
            self._result.error_message = TspiotResponseMessages.CONNECTION_ERROR.value
        except Exception as e:
            self._result.error_message = f"{TspiotResponseMessages.CRITICAL_ERROR_PREFIX.value}{e}"

        self._result.success = False
        logger.error(self._result.error_message)
        return self._result



    def close(self):
        """Закрывает клиент"""
        self._close_client()

    def __del__(self):
        self.close()
