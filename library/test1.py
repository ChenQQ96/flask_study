#使输出的html应用看起来更复杂一些
#能接受内部参数
from flask import Flask,render_template
import datetime

app=Flask(__name__)

@app.route('/1/')
def index_v1():
    """
    params：
        user:输入参数——用户名
        html_text:响应值
    """
    user={'username':"ChenQQ"}
    html_text="""
    <html>
        <head>
            <title>inner flask page</title>
        </head>
        <body>
            <h3>hello,"""+user['username']+"""</h3> <!--固定格式-->
        </body>
    </html>
    """
    return html_text

@app.route('/2/')
def index_v2():
    """
    实现python代码和html页面的参数传递
    实现前、后端分离
    """
    user={'username':"ChenQQ"}
    return render_template('index_v2.html',title='ChenQQ',user=user)

@app.route('/3/')
def index_v3():
    """
    产生更多参数，html页面更复杂，实现if else loop循环等基本业务
    """
    user={'username':"ChenQQ"}
    borrower={'postcard':"111","borrowdate":"2021-09-22"}
    booklist=[
        {"author":"name1","bookname":"book1"},
        {"author":"name2","bookname":"book2"},
        {"author":"name3","bookname":"book3"},
        {"author":"name4","bookname":"book4"}
    ]
    return render_template("index_v3.html",title="title",borrower=borrower,booklist=booklist)

@app.route('/4/')
def index_v4():
    """继承"""
    today=datetime.date.today()
    user={'username':"ChenQQ"}
    borrower={'postcard':'222','borrowdate':today}
    tabletitle={'author','bookname'}
    booklist=[
        {"author":"name1","bookname":"book1"},
        {"author":"name2","bookname":"book2"},
        {"author":"name3","bookname":"book3"},
        {"author":"name4","bookname":"book4"}
    ]
    return render_template('index_v4.html',user=user,borrower=borrower,tabletitle=tabletitle,booklist=booklist)

@app.route('/test1/')
def test1():
    title="test1"
    username={"name1":"ChenQQ"}
    return render_template('test1.html',title=title,username=username)

@app.route('/test2/')
def test2():
    today=datetime.date.today()
    title="test2"
    user={'username':'ChenQQ'}
    borrower={'postcard':'11',"borrowdate":today}
    booklist=[
        {'author':'name1','bookname':'book1'},
        {'author':'name2','bookname':'book2'}
    ]
    return render_template('test2.html',title=title,borrower=borrower,booklist=booklist)

if __name__=="__main__":
    app.run()