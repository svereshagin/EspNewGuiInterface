import logging
from typing import Optional
import httpx
from src.dto.kkt import CashInfo
from src.network.base import ApiClient

logger = logging.getLogger(__name__)



class KKTNetwork(ApiClient):
    _DKKT_URL = "/api/v1/dkktList"
    READ_TIMEOUT = 60.0

    def get_dkkt_list(self) -> Optional[CashInfo]:
        logger.debug("Запрос к %s", self._DKKT_URL)
        try:
            response = self.get(self._DKKT_URL)
            if response.status_code == 200:
                cash_info = CashInfo.from_api_response(response.json())
                print(cash_info)
                logger.info("Получено касс: %d", len(cash_info.kkt))
                return cash_info

            logger.warning("Статус %s от оркестратора", response.status_code)
            return None

        except httpx.TimeoutException:
            logger.error("Таймаут при запросе к %s", self._DKKT_URL)
            return None
        except httpx.ConnectError:
            logger.error("Нет соединения с оркестратором")
            return None
        except Exception as e:
            logger.exception("Ошибка при запросе списка касс %s", e)
            return None


