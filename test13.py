#关键字with的用法
#断言assert的用法

#用法1：打开文件
with open('test5.py') as f:
    r=f.read()
print(r)
print('------------------')
#相当于try except finally

try:
    f=open('test5.py')
    p=f.read()
except:
    pass
finally:
    f.close()
print(p)
print('------------------')

assert False