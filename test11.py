from flask import make_response,Flask,render_template
import time
app=Flask(__name__)

@app.route('/')
def index():
    class Person(object):
        Email = 'XXX@XXX.com'
        time = time.time()

    dell=Person()

    context={
        'username':"王亚锋",
        'age': "18",
        'gender': "男",
        'flag': "王者",
        'hero': "猴子",
        'person':dell,
        'wwwurl':{
            'baidu':'www.baidu.com',
            'google':'www.google.com'
        }
    }
    return render_template('index.html',**context)

app.run()