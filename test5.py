from functools import partial
def multi(x,y):
    print("x = {},y = {}".format(x,y))
    print(x*y)

double=partial(multi,y=2) #返回函数,其中y=2
double(1)