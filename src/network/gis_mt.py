1.2.19.	Запрос на получение настроек ЕСМ
Запрос GET на endpoint /api/v1/settings/:id
Где :id это идентификатор инстанса ЕСМ
Пример запроса:
curl --location 'http://127.0.0.1:51077/api/v1/settings/0128245621'

Пример ответа:
{"compatibilityMode":false,"allowRemoteConnection":false,"gismtAddress":"https://tsp-test.crpt.ru:19100"}
Поля ответа:
Параметр	Тип	Описание
compatibilityMode	boolean	режим совместимости для оффлайн запросов
allowRemoteConnection	boolean	режим удаленного подключения (возможность подключаться с внешних IP)
gismtAddress	string	адрес ГИС МТ
