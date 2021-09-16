#知道一个函数，怎么去获得这个URL呢:通过 url_for(函数名,查询参数)
from flask import Flask,url_for,request

app = Flask(__name__)

@app.route('/',methods=['POST','GET'])
def index():
    if request.method=='POST':
        return 'POST'
    else:
        return 'GET'

@app.route('/login/')
def login():
    return 'login'

@app.route('/user/<username>/')
def user(username):
    return 'Welcome, {}'.format(username)


#url_for这个函数正确运行需要上下文的支持，也就是说要保证url_for这个函数所处的地方必须是一个app里面
#当写在某个响应函数中没有问题,如果在app外面使用url_for的话,可以使用with关键字指定上下文.
with app.test_request_context():
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('user',username='ChenQQ'))

app.run()