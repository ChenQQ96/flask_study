from time import time,sleep
from functools import wraps #可以通过使用Python自带模块functools中的wraps来保留函数的元信息

def run_time(func):
    def wrapper(*args,**kw):
        start=time()
        func()
        end=time()
        cost_time=end-start
        print("func run time {}".format(cost_time))
    return wrapper

@run_time
def func():
    sleep(1)

func()
print(func.__name__)

def run_time2(func):
    @wraps(func)   #<- 在这里加wraps(func)，即可
    def wrapper(*args,**kw):
        start=time()
        func()
        end=time()
        cost_time=end-start
        print("func run time {}".format(cost_time))
    return wrapper

@run_time2
def func2():
    sleep(2)

func2()
print(func2.__name__)
