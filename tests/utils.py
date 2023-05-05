from time import sleep


def work_sleep(sec: int) -> str:
    sleep(sec)
    return "Wake Up"
