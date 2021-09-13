from base_api import *
from time import time, sleep

def run_time(func):
    """
    不带参数的装饰器
    """
    def wrapper():
        start = time()
        func()                  # 函数在这里运行
        end = time()
        cost_time = end - start
        print("func three run time {}".format(cost_time))
    return wrapper

@run_time
def fun_one():
    sleep(2)

fun_one()
