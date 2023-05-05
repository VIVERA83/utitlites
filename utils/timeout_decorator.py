"""Декоратор, который ограничивает время выполнения функции."""
from functools import wraps
from typing import Callable
import signal


def timeout(time_out: int = 2, timeout_error: bool = True):
    """Декоратор, который ограничивает время выполнения функции.

    Если функция не успела завершиться за заданное время - `time_out`
    выполнение функции будет остановлено. После в зависимости от параметра
    `timeout_error`:
        True: будет инициализировано исключение TimeoutError.
        False: вернет None.

    :param time_out: Количество секунд, которым ограничивается время выполнения функции.
    :param timeout_error: При истечении времянки выбрасывать ошибку TimeoutError или нет
    :return:
    """

    def timeout_handler(*_):
        raise TimeoutError

    def wrapper(func: Callable):
        @wraps(func)
        def inner(*args, **kwargs):
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(time_out)
            try:
                return func(*args, **kwargs)
            except TimeoutError:
                if timeout_error:
                    raise TimeoutError
            finally:
                signal.alarm(0)

        return inner

    if time_out < 1:
        raise ValueError("time_out must be greater than 0")

    return wrapper
