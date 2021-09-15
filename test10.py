#一个最简单的Flask的web应用

from flask import Flask

app = Flask(__name__) #__name__是python模块名

#定义路由规则
#'/'指明了当地址是根路径时，就调用下面的函数
#将URL和执行的视图函数的关系保存到app.url_map属性上
#当请求的地址符合路由规则时，就会进入该函数;在里面获取请求的request对象，返回的内容就是response。本例中的response就是大标题”hello world!”
@app.route('/1')
def func():
    return 'hello world!'

#唯一URL规则--@app.route('/', endpoint='1')
@app.route('/2')
def func2():
    return 'bad'

@app.route('/user/<name>')
def user(name):
    return 'Hello, {}!'.format(name)

if __name__=='__main__':
    #启动Web服务器
    #Web服务器会默认监听本地的5000端口，但不支持远程访问。如果你想支持远程，需要在run()方法传入host=0.0.0.0，想改变监听端口的话，传入port=端口号
    #Flask自带的Web服务器主要还是给开发人员调试用的，在生产环境中，你最好是通过WSGI将Flask工程部署到类似Apache或Nginx的服务器上
    app.run(host='0.0.0.0',port=10000)