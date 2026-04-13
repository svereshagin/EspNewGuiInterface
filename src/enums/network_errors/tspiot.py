import enum


class TspiotResponseMessages(enum.Enum):
    """Константы сообщений — удобно для локализации в будущем"""
    TIMEOUT_ERROR = "Превышено время ожидания ответа от оркестратора"
    CONNECTION_ERROR = "Не удалось установить соединение с оркестратором"
    REQUEST_ERROR_PREFIX = "Ошибка выполнения запроса: "
    MISSING_FIELDS = "В ответе отсутствуют поля 'id' и/или 'serviceState'"
    NON_201_RESPONSE = "Сервер вернул код"
    JSON_PARSE_ERROR = "Не удалось разобрать JSON-ответ"
    CRITICAL_ERROR_PREFIX = "Критическая ошибка при создании TSPIOT.qml: "
    SUCCESS_PREFIX = "TSPIOT.qml успешно запущен → id="
    UNEXPECTED_STATUS_PREFIX = "Сервис находится в состоянии"

