#理解@app.route()

class FlaskBother():
    def __init__(self):
        self.routes={}

    def route(self,route_str):
        """
        将路由和关联的函数保存到我们的 "route" 字典中去
        """
        def decorator(func):
            self.routes[route_str]=func
            return func
        return decorator

    def server(self,path):
        """
        可以访问内部 route 
        通过路由去访问其关联的函数;如果没有的话,返回一个错误
        """
        view_function=self.routes.get(path) #字典get()语法：dict.get(key,default=None)
        if view_function:
            return type(view_function)
        else:
            raise ValueError('Route "{}" has not been registered'.format(path))

app = FlaskBother()
@app.route('/hello')
def hello():
    return "Hello world"


app.server('/hello')