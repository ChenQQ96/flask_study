#函数嵌套

print('函数嵌套')
def outer():
    name = "python"
    def inner():
        print('name')
    return inner()#对于outer函数中最后一句，返回inner函数调用的结果
outer()

print('-----------------------------')
print('return内层函数时不加括号，只返回函数的地址')
def outer2():
    name = "python"
    def inner():
        print('name')
    return inner

print('函数inner的地址为：{}'.format(outer2()))
print('想要执行内层函数，需要在outer()后边再加个括号，即outer()()，才会让内层函数执行')
print('函数inner的运行结果为: ')
outer2()()
print('------------------------------')
