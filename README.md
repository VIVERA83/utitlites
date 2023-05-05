# Полезные утилиты

Репозиторий посвящен утилитам которые были написаны мной и используются в некоторых моих проектах.

<span id="0"></span>

1. [timeout](#1) - принудительно завершает исполнение функции или другого вызываемого объекта
2. [.gitignore](#6)

___

### <span id="1">1. </span><span style="color:purple">timeout</span>

</span><span style="color:orange">__Описание:__</span>

Декоратор, который принудительно останавливает и завершает выполнение вызываемого объекта.

Бывает так что выполнение функции может зависнуть по разным причинам, например ждет ответа от удавленного источника,
либо выполняет сложную вычислительную операцию, а времянки ждать результата нет. А бывает так что функция может
некорректно работать и зациклится в вечный цикл. Либо в тестах необходимо ограничить время исполнения вызываемой
функции.
Для таких случаев можно попробовать использовать timeout.

Листинг функции можно посмотреть [тут](utils%2Ftimeout_decorator.py)

Например:

* функция
* экземпляр(объекта) класса с объявленным
  методом `__call__`, подробнее о `__call__`
  смотри [тут](https://proproprogs.ru/python_oop/magicheskiy-metod-call-funktory-i-klassy-dekoratory?ysclid=lhacw8ssek103695718)
* метод экземпляра(объекта) класса
  Корректно работать с асинхронными функциями не будет, так как является обычным декоратором без поддержки асинхронного
  исполнения.
  Да и для остановки асинхронных функций есть несколько способов. Подробности можно посмотреть
  в [asyncio](https://docs.python.org/3/library/asyncio-task.html)
  или [тут](https://docs-python.ru/standart-library/modul-asyncio-python/funktsija-wait-for-modulja-asyncio/)

</span><span style="color:orange">__Пример использования:__</span>

```python
from utils.timeout_decorator import timeout
from time import sleep


def work_sleep(sec: int) -> str:
    sleep(sec)
    return "Wake Up"


@timeout(timeout_error=False)
def work_sleep_2(sec: int) -> str:
    sleep(sec)
    return "Wake Up"


if __name__ == '__main__':
    work_1 = timeout(time_out=2)(work_sleep)
    print(work_sleep_2(1))  # Wake Up
    print(work_sleep_2(3))  # None
    print(work_1(3))  # raise TimeoutError

```

Так же примеры использования можно посмотреть [тут](examples%2Ftimeout_decorator.py)

### [Наверх](#0) [&#9757;](#0)

----
&#129657;




