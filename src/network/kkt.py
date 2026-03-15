1.2.16.	Запрос на установку настроек ЛМ
Запрос PUT на endpoint /api/v1/settings/lm/:id
Где :id это идентификатор инстанса ЕСМ
Примеры запроса:
curl --location --request PUT 'http://127.0.0.1:51077/api/v1/settings/lm/00106329566391' --header 'Content-Type: application/json' --data '{"address":"10.9.130.12","port":50063,"login":"admin","password":"admin"}'

Поля запроса:
Параметр	Тип	Описание
address	string	IP адрес контролера ЛМ ЧЗ
port	number	порт контролера ЛМ ЧЗ
login	string	логин ЛМ ЧЗ
password	string	пароль ЛМ ЧЗ
newPassword	string	новый парольь для ЛМ ЧЗ
