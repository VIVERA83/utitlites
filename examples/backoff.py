import asyncio
from asyncio import Event
from typing import Any
from loguru import logger
from utils.backoff import before_execution
import logging


@before_execution(total_timeout=2, request_timeout=1, logger=logger, raise_exception=True)
async def division(a: float, b: float) -> float:
    """Деление двух чисел.

    Деление числа a на b. Без проверки делителя на 0 возникает ошибка.,
    да и вообще при попытке передачи параметров отличающихся от чисел будет
    инициализирована ошибка"""
    return a / b


@before_execution(total_timeout=15, request_timeout=1, logger=logger, raise_exception=True)
async def connect_to_some_api(event: Event):
    """Имитация подключения к удаленному серверу.

    Предположим, идёт подключение к ElasticSearch в момент запуска docker compose файла.
    Как известно depends_on - не дожидается полной загрузки зависимости, и может случиться такая ситуация
    когда ElasticSearch полностью еще не прогрузился, а приложение уже пытается подключиться к серверу.
    В таком случае вылетает исключение и приложение вероятнее всего корректно работать уже не будет.
    """
    # имитация подключения к удаленному серверу
    # request_timeout = 1 - не даст долго ждать подключения, поэтому выполнение функции будет перервано по тайм-ауту,
    # в реальности же вывалится ошибка типа ConnectionError.
    # Но так как функция задекорирована `before_execution` через request_timeout=1,
    # будет совершена еще одна попытка выполнить подключение (исполнить эту функцию).
    # И так будет продолжаться пока функция не выполнится, либо не закончится отведенное время на подключение
    # которое равно total_timeout=15.
    await event.wait()
    print("Connect to ElasticSearch is successful")


async def fake_elastic_search(event: Event):
    # Предположим это время требующие для полного запуска ElasticSearch
    await asyncio.sleep(10)
    # Это блокиратор событий, пока он не равен True, все кто находится в await event.wait() будут ждать.
    # В нашем случае это сonnect_to_some_api, которая имитирует подключение к удаленному серверу.
    event.set()  # Переводим в True
    print("Elastic Search is ready")


async def main(a: Any, d: Any):
    ready = asyncio.Event()
    await asyncio.gather(fake_elastic_search(ready), connect_to_some_api(ready))


if "__main__" == __name__:
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main(10, 0))
