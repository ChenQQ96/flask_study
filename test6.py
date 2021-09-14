#setattr和getattr函数
#getattr:用于获取属性值，该属性一定是存在的。
#setattr:用于设置属性值，该属性不一定是存在的。
#getattr语法：getattr(object,name)
#setattr语法：setattr(object,name,value)

class A:
    name = "a"

B=A()
print("name is {}".format(getattr(B,'name')))

setattr(A,'age',1)
C=A()
print("name is {},age is {}".format(getattr(C,'name'),getattr(C,'age')))