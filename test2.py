from base_api import *
from time import time, sleep

def logger(msg=None): #装饰器的参数
    """
    带参数的装饰器
    params:
        msg
    """
    def run_time(func):
        def wrapper(*args,**kw):
            """
            params:
                #args,**kw:func函数的参数
            """
            start = time()
            func()
            end = time()
            cost_time=end-start
            print("[{}] func three run time {}".format(msg, cost_time))
        return wrapper
    return run_time

@logger(msg="One") #装饰器的参数
def func_one():
    sleep(1)

@logger(msg="Two")
def func_two():
    sleep(2)

func_one()
func_two()