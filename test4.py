#对装饰器添加一些属性，就如同给一个类定义实现不同功能的方法那样。
import logging
from functools import partial
logging.basicConfig(
    # filename='my.log',
    level=logging.INFO,
    format='%(asctime)s %(filename)s +%(lineno)s: %(levelname)-8s %(message)s'
    )

def  logger_error(func):
    logmsg=func.__name__
    def wrapper():
        func()
        logging.log(logging.ERROR,"{} if over".format(logmsg)) #logging.log(level,logmsg)
    return wrapper

@logger_error
def func():
    print("func")

func()

print('---------------------------------------------------')

# 作者：Jackpop
# 链接：https://www.zhihu.com/question/325817179/answer/798679602
# 来源：知乎
# 著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

def wrapper_property(obj, func=None):
    if func is None:
        return partial(wrapper_property,obj)
    setattr(obj, func.__name__,func)
    return func

def logger_info(level, name=None, message=None):
    def decorate(func):
        logmsg = message if message else func.__name__

        def wrapper(*args, **kwargs):
            logging.log(level, logmsg)
            return func(*args, **kwargs)

        @wrapper_property(wrapper)
        def set_level(newlevel):
            nonlocal level
            level = newlevel

        @wrapper_property(wrapper)
        def set_message(newmsg):
            nonlocal logmsg
            logmsg = newmsg

        return wrapper
    return decorate

@logger_info(logging.INFO)
def main(x, y):
    return x + y #这里面最重要的是wrapper_property这个函数，它的功能是把一个函数func编程一个对象obj的属性，然后通过调用wrapper_property，给装饰器添加了两个属性set_message和set_level，分别用于改变输出日志的内容和改变输出日志的等级。看一下输出结果，main(3, 3)

print(main(3,3))
# 输出
# WARNING:Test:main
# 6
# Example use

