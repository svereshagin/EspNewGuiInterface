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
    NON_200_RESPONSE = "Сервер вернул код"
    JSON_PARSE_ERROR = "Не удалось разобрать JSON-ответ"
    CRITICAL_ERROR_PREFIX = "Критическая ошибка при создании tspiot: "
    SUCCESS_PREFIX = "tspiot успешно запущен → id="
    UNEXPECTED_STATUS_PREFIX = "Сервис находится в состоянии"


@dataclass
class RequestCreateInstanceTSPIOT_DTO:
    id: str #идентификатор инстанса ЕСМ заполняется значением kktSerial из списка ДККТ
    port: int | None #порт для подключения оркестратора
    softPort: int | None #ПОРТ ДЛЯ ПМСР


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



    def __init__(self):
        self._result: TspiotResult = TspiotResult()

    def get_result(self) -> TspiotResult:
        return self._result

    def execute(self, data: RequestCreateInstanceTSPIOT_DTO) -> TspiotResult:
        """
        Выполняет POST-запрос и проверяет результат запуска сервиса
        """
        self._result = TspiotResult()  # сброс результата

        if not data.id:
            self._result.error_message = "Передан пустой tspiot_id"
            logger.error(self._result.error_message)
            return self._result

        payload = {"id": data.id}
        if data.softPort:
            payload["softPort"] = data.softPort
        if data.port:
            payload["port"] = data.port
        try:
            with ApiClient() as client:
                response: httpx.Response = client.post(
                    self.ENDPOINT,
                    data=payload
                )

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
            # непредвиденная ошибка до получения ответа
            self._result.error_message = (
                TspiotResponseMessages.CRITICAL_ERROR_PREFIX.value + str(e)
            )
            logger.exception(self._result.error_message)
            return self._result

        # ────────────────────────────────────────────────
        # Обработка ответа
        # ────────────────────────────────────────────────

        logger.debug(f"POST {self.ENDPOINT} → статус {response.status_code}")

        if response.status_code != 200:
            msg = f"{TspiotResponseMessages.NON_200_RESPONSE.value} {response.status_code}"
            try:
                detail = response.json().get("detail", "").strip()
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


# ────────────────────────────────────────────────
# Пример использования / тестовый запуск
# ────────────────────────────────────────────────

