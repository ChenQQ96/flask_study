#global:如果局部要对全局变量修改，应在局部声明该全局变量。 
#nonlocal：声明的变量不是局部变量,也不是全局变量,而是外部嵌套函数内的变量。
print('不使用global，会报错')
try:
    count = 0
    def global_test():
        count += 1
        print(count)

    global_test()
except UnboundLocalError as e:
    print(e)

print('----------------------------------')
print('使用global')
count=0
def global_test():
    global count
    count+=1
    print(count)
global_test()
global_test()

print('---------------------------------')
print(' 如果局部不声明全局变量，并且不修改全局变量，则可以正常使用。')
def global_test2():
    print(count)
global_test2()
print('---------------------------------')

print('使用nonlocal')
def nonlocal_test():
    count=0
    def test():
        nonlocal count
        count+=1
        return count
    return test

val = nonlocal_test()
print(val())
print(val())
print(val())