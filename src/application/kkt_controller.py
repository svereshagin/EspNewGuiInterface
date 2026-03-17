# логика
#
# есть dkktList запрос
#
# он возвращает доступные нам кассы
#
# далее мы помещаем каждую кассу в список касс
#
# выводим кассы в dkktList
#
# при нажатии на Обновить -> происходит вызов данного функционала
#
# устанавливаем логику распознавания работы с controlmodule
from src.network.kkt import KKTNetwork


class KKTController:
    KKT_NETWORK = KKTNetwork()
    result = KKT_NETWORK.get_dkktList()
    print(result)

if __name__ == '__main__':
    KKTController()