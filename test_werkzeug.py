from base_api import *

from werkzeug.wrappers import Request,Response
from werkzeug.serving import run_simple
#wsgi.py
#werkzeug是一个用于编写Python WSGI程序的工具包
#它的结构设计和代码质量在开源社区广受褒扬，其源码被尊为Python技术领域最值得阅读的开源库之一

@Request.application
def hello(request):
    return Response("Hello World")

if __name__ == '__main__':
    #请求一旦到来，执行第3个参数，hello(上下文)
    run_simple('localhost', 4000, hello)