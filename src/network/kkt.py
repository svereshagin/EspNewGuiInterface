import httpx

from src.core.config import ApiSettings
from src.network.base import ApiClient


class KKTNetwork(ApiClient):
    __DKKT_URL = "/api/v1/dkktList"
    config = ApiSettings()

    def get_dkktList(self):
        """Использование с контекстным менеджером"""

        with ApiClient() as client:
            response = client.get(self.__DKKT_URL)
            print(f"Статус: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"Данные: {data}")



# 1.2.16.	Запрос на установку настроек ЛМ
# Запрос PUT на endpoint /api/v1/settings/lm/:id
# Где :id это идентификатор инстанса ЕСМ
# Примеры запроса:
# curl --location --request PUT 'http://127.0.0.1:51077/api/v1/settings/lm/00106329566391' --header 'Content-Type: application/json' --data '{"address":"10.9.130.12","port":50063,"login":"admin","password":"admin"}'
#
# Поля запроса:
# Параметр	Тип	Описание
# address	string	IP адрес контролера ЛМ ЧЗ
# port	number	порт контролера ЛМ ЧЗ
# login	string	логин ЛМ ЧЗ
# password	string	пароль ЛМ ЧЗ
# newPassword	string	новый парольь для ЛМ ЧЗ
