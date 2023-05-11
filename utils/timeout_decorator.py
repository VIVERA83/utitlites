"""Декоратор, который ограничивает время выполнения функции."""
from functools import wraps
from typing import Callable
import signal
import sys
import threading

__all__ = ["timeout"]

if sys.platform == "win32":
    def timeout(delay_time: int = 2, timeout_error: bool = True):
        """Декоратор, который ограничивает время выполнения функции.

        Если функция не успела завершиться за заданное время - `time_out`
        выполнение функции будет остановлено. После в зависимости от параметра
        `timeout_error`:
            True: будет инициализировано исключение TimeoutError.
            False: вернет None.

        :param delay_time: Количество секунд, которым ограничивается время выполнения функции.
        :param timeout_error: При истечении времянки выбрасывать ошибку TimeoutError или нет
        :return:
        """

        def wrapper(func: Callable):
            @wraps(func)
            def inner(*args, **kwargs):
                result = None
                is_time_out = True

                def handler():
                    nonlocal result, is_time_out
                    result = func(*args, **kwargs)
                    is_time_out = False

                thread = threading.Thread(name='TIMEOUT', target=handler, daemon=True)
                thread.start()
                thread.join(delay_time)
                if is_time_out and timeout_error:
                    raise TimeoutError
                return result

            return inner

        if delay_time < 1:
            raise ValueError("time_out must be greater than 0")

        return wrapper


else:
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
            raise ValueError("`delay_time` must be greater than 0")

        return wrapper
