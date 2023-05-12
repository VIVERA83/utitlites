"""Проверка работы декоратора  before_execution."""
import asyncio
from asyncio import Event

import pytest

from tests.utils import connect_to_database, division, fake_database
from utils.backoff import before_execution


class TestBeforeExecution:
    """Проверка работы декоратора  before_execution."""

    async def test_errors(self):
        """Проверка на исключения.

        Проверка обработки исключения в обернутой функции"""

        with pytest.raises(ZeroDivisionError):
            await before_execution(1, raise_exception=True)(division)(
                1, 0, time_delta=0
            )
        assert not await before_execution(1, raise_exception=False)(division)(
            1, 0, time_delta=0
        )

    async def test_success(self):
        """Проверка на успешное завершение"""

        assert 1 == await before_execution(1)(division)(1, 1, time_delta=0)

    async def test_after_exclusion(self):
        """Проверка на исполнение, после ошибки.

        Проверка на то как исполняется обернутая функция
        после неудачная попытка выполнится.
        """
        event = Event()
        connect = before_execution()(connect_to_database)(event)
        assert (
            "Connect successfully"
            == (
                await asyncio.gather(connect, fake_database(event=event, time_delta=3))
            )[0]
        )
