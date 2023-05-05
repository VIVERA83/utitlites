"""Проверка работы декоратора timeout."""
import pytest

from utils.timeout_decorator import timeout
from tests.utils import work_sleep


class TestTimeoutDecorator:
    """Проверка работы декоратора timeout."""

    def test_timeout_error(self):
        """Проверка на вывод исключения TimeError.

        При превышении времянки выполнения функции, заданного в параметре `time_out`,
        должно генерироваться исключение TimeError, если параметр `timeout_error` = True.
        Параметр `timeout_error` должен иметь значение True.
        """
        work_1 = timeout()(work_sleep)
        work_2 = timeout(3)(work_sleep)
        with pytest.raises(TimeoutError):
            work_1(3)
            work_2(3)

    def test_value_error(self):
        """Проверка на вывод исключения ValueError.

        При попытках передать параметру `time_out` значение менее 1,
        должно генерироваться исключение ValueError.
        """
        with pytest.raises(ValueError):
            timeout(0)(work_sleep)

    def test_return_data(self):
        """Проверка на вывод результата.

        1. Успешное выполнение функции за заданное время time_out`.
        1. Функция не успела закончить исполнение за отведенное время `time_out`.
        """

        work_1 = timeout()(work_sleep)
        work_2 = timeout(time_out=1, timeout_error=False)(work_sleep)
        assert work_1(1) == "Wake Up"
        assert work_2(3) is None
