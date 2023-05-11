from utils.timeout_decorator import timeout
from time import sleep, time


def work_sleep(sec: int) -> str:
    sleep(sec)
    return "Wake Up"


@timeout(timeout_error=False)
def work_sleep_2(sec: int) -> str:
    sleep(sec)
    return "Wake Up"


@timeout(delay_time=5, timeout_error=False)
def forever_lasting():
    start = time()
    while True:
        sleep(1)
        print("I'm working already: {} sec.".format(time() - start))
    return "It will never come"


if __name__ == '__main__':
    # вариант оборачивания функции в декоратор
    work_1 = timeout(delay_time=2)(work_sleep)
    # Вариант оборачивания функции в декораторе. Немедленный вызов
    timeout(delay_time=2, timeout_error=False)(work_sleep)(2)
    print(work_sleep_2(1))  # Wake Up
    print(work_sleep_2(3))  # None
    try:
        print(work_1(3))  # raise TimeoutError
    except TimeoutError:
        print("Timeout...")
    print(forever_lasting())  # None
    # I'm working already: 1.0012803077697754 sec.
    # I'm working already: 2.0013651847839355 sec.
    # I'm working already: 3.0020499229431152 sec.
    # I'm working already: 4.002134084701538 sec.
    # I'm working already: 5.0026514530181885 sec.

