import enum
import logging
from dataclasses import dataclass
from typing import Optional

import httpx

from src.core.config import ApiSettings
from src.network.base import ApiClient

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
    tspiotId: str


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



    def register_tspiot(self, data: RequestRegistrationTSPIOT_DTO):
        """Регистрирует TSPIOT"""
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
                json=payload  # Используем json, а не data
            )
            logger.debug(f"PUT {self.ENDPOINT} → статус {response.status_code}")

            data = response.json()

            if response.status_code == 200:
                result_data = response.json()
                return ResponseRegistrationTSPIOT_DTO(tspiotId=result_data.get("tspiotId"))
            if response.status_code == 400 and data.get("code") == 1010: #всё ОК, иногда тспиот залагивает и лучше отдельно чекнуть этот вариант позже
                return {
                    'success': True,
                }

            elif response.status_code == 403:
                # Ошибка от оркестратора = несколько ИНН
                error_data = response.json()
                logger.warning(f"Ошибка регистрации: {error_data}")
                return {
                    'success': False,
                    'error_message': error_data.get('error', {}).get('text', 'Неизвестная ошибка')
                }
            else:
                logger.error(f"Ошибка регистрации: статус {response.status_code}, тело: {response.text}")
                return {
                    'success': False,
                    'error_message': f"HTTP {response.status_code}: {response.text}"
                }

        except httpx.TimeoutException:
            logger.error(TspiotResponseMessages.TIMEOUT_ERROR.value)
            return {
                'success': False,
                'error_message': TspiotResponseMessages.TIMEOUT_ERROR.value
            }
        except httpx.ConnectError:
            logger.error(TspiotResponseMessages.CONNECTION_ERROR.value)
            return {
                'success': False,
                'error_message': TspiotResponseMessages.CONNECTION_ERROR.value
            }
        except Exception as e:
            logger.error(f"Ошибка регистрации: {e}")
            return {
                'success': False,
                'error_message': str(e)
            }

    def get_result(self) -> TspiotResult:
        return self._result

    def create_esm_service(self, data: RequestCreateInstanceTSPIOT_DTO) -> TspiotResult:
        """
        Выполняет POST-запрос и проверяет результат запуска сервиса
        """
        self._result = TspiotResult()  # сброс результата

        if not data.kkt_serial:
            self._result.error_message = "Передан пустой kkt_serial"
            logger.error(self._result.error_message)
            return self._result

        payload = {"id": data.kkt_serial}

        # оставил для обратной совместимости, в протоколе две версии
        if data.softPort:
            payload["softPort"] = data.softPort
        if data.port:
            payload["port"] = data.port

        client = self._get_client()

        try:
            response = client.post(
                self.ENDPOINT,
                json=payload  # Используем json, а не data
            )
            logger.debug(f"POST {self.ENDPOINT} → статус {response.status_code}")

        except httpx.TimeoutException:
            self._result.error_message = TspiotResponseMessages.TIMEOUT_ERROR.value
            logger.error(self._result.error_message)
            return self._result

        except httpx.ConnectError:
            self._result.error_message = TspiotResponseMessages.CONNECTION_ERROR.value
            logger.error(self._result.error_message)
            return self._result

        except httpx.RequestError as e:
            self._result.error_message = (
                    TspiotResponseMessages.REQUEST_ERROR_PREFIX.value + str(e)
            )
            logger.error(self._result.error_message)
            return self._result

        except Exception as e:
            self._result.error_message = (
                    TspiotResponseMessages.CRITICAL_ERROR_PREFIX.value + str(e)
            )
            logger.exception(self._result.error_message)
            return self._result

        # Обработка ответа
        if response.status_code != 201:
            msg = f"{TspiotResponseMessages.NON_201_RESPONSE.value} {response.status_code}"

            try:
                error_data = response.json()
                detail = error_data.get("detail", "")
                if detail:
                    msg += f" → {detail}"
                elif response.text:
                    msg += f" → {response.text[:180]}..."
            except Exception:
                if response.text:
                    msg += f" → {response.text[:180]}..."

            self._result.error_message = msg
            logger.error(self._result.error_message)
            return self._result

        # Парсинг JSON
        try:
            data = response.json()
        except Exception as e:
            self._result.error_message = (
                f"{TspiotResponseMessages.JSON_PARSE_ERROR.value} — {e}"
            )
            logger.error(self._result.error_message)
            return self._result

        # Проверка обязательных полей
        if "id" not in data or "serviceState" not in data:
            self._result.error_message = TspiotResponseMessages.MISSING_FIELDS.value
            logger.error(self._result.error_message + f" → получено: {data}")
            return self._result

        self._result.tspiot_id = str(data["id"])
        self._result.status = str(data["serviceState"])

        if self._result.status == "Работает":
            self._result.success = True
            self._result.error_message = None
            logger.info(
                f"{TspiotResponseMessages.SUCCESS_PREFIX.value}{self._result.tspiot_id}"
            )
        else:
            self._result.error_message = (
                f"{TspiotResponseMessages.UNEXPECTED_STATUS_PREFIX.value} "
                f"'{self._result.status}' (ожидалось 'Работает')"
            )
            logger.warning(self._result.error_message)

        return self._result

    def close(self):
        """Закрывает клиент"""
        self._close_client()

    def __del__(self):
        self.close()
