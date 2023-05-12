import asyncio
from asyncio import Event
from time import sleep


def work_sleep(sec: int) -> str:
    sleep(sec)
    return "Wake Up"


async def division(a: float, b: float, time_delta: int) -> float:
    """Деление двух чисел.

    Деление числа a на b"""
    sleep(time_delta)
    return a / b


async def connect_to_database(event: Event):
    """Имитация подключения к удаленному серверу."""

    await event.wait()
    return "Connect successfully"


async def fake_database(event: Event, time_delta: int):
    """Имитация запуска базы данных.

    Предположим некая база данных перезапускается,
    для готовности ей требуется какое-то время.
    """
    await asyncio.sleep(time_delta)
    event.set()
    return "Database ready"
