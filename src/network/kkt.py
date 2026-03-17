import httpx
from typing import Optional

from domain.kkt.entity import CashInfo
from src.core.config import ApiSettings
from src.domain.common.regime_local_module import KktInfo
from src.network.base import ApiClient


class KKTNetwork(ApiClient):
    __DKKT_URL = "/api/v1/dkktList"
    __SETTINGS_LM_URL = "/api/v1/settings/lm"
    config = ApiSettings()

    def __init__(self):
        super().__init__()
        self._client = None  # Сохраняем клиент для повторного использования

    def _get_client(self):
        """Получает или создает HTTPX клиент"""
        if self._client is None or self._client.is_closed:
            # Создаем клиент без контекстного менеджера
            self._client = httpx.Client(
                base_url=self.config.orchestrator_url,
                timeout=30.0
            )
            print("✅ Создан новый HTTPX клиент")
        return self._client

    def get_dkktList(self) -> CashInfo | None:
        """Получение списка касс"""
        try:
            client = self._get_client()
            response = client.get(self.__DKKT_URL)
            print(f"Статус: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                cash_info = CashInfo.from_api_response(data)
                print(f"Данные: {cash_info}")
                return cash_info
            else:
                print(f"Ошибка API: статус {response.status_code}")
                print(f"Ответ: {response.text}")
                return None

        except httpx.TimeoutException as e:
            print(f"Таймаут соединения: {e}")
            return None
        except httpx.NetworkError as e:
            print(f"Сетевая ошибка: {e}")
            return None
        except httpx.HTTPStatusError as e:
            print(f"HTTP ошибка: {e.response.status_code} - {e.response.text}")
            return None
        except httpx.RequestError as e:
            print(f"Ошибка запроса: {e}")
            return None
        except ValueError as e:
            print(f"Ошибка парсинга JSON: {e}")
            return None
        except Exception as e:
            print(f"Неизвестная ошибка: {e}")
            return None

    def set_lm_settings(self, lm_id: str, address: str, port: int,
                        login: str, password: str, new_password: str = None) -> bool:
        """
        Установка настроек ЛМ
        PUT /api/v1/settings/lm/:id
        """
        try:
            client = self._get_client()
            url = f"{self.__SETTINGS_LM_URL}/{lm_id}"

            # Формируем данные запроса
            data = {
                "address": address,
                "port": port,
                "login": login,
                "password": password
            }

            # Добавляем новый пароль, если передан
            if new_password:
                data["newPassword"] = new_password

            response = client.put(url, json=data)
            print(f"Статус установки настроек ЛМ: {response.status_code}")

            if response.status_code in [200, 201, 204]:
                print(f"✅ Настройки ЛМ успешно установлены для {lm_id}")
                return True
            else:
                print(f"❌ Ошибка установки настроек: {response.status_code}")
                print(f"Ответ: {response.text}")
                return False

        except Exception as e:
            print(f"❌ Ошибка при установке настроек ЛМ: {e}")
            return False

    def close(self):
        """Закрывает клиент при завершении работы"""
        if self._client and not self._client.is_closed:
            self._client.close()
            print("🔒 HTTPX клиент закрыт")

    def __del__(self):
        """Деструктор для гарантированного закрытия"""
        self.close()