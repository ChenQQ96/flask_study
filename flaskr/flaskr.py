#所有导入的模块(all the imports)
import sqlite3
from flask import Flask,request,session,g,redirect,url_for,abort,render_template,flash

#初始化数据库
from contextlib import closing

#配置参数(configuration)
DATABASE = 'templates/flaskr.db'
DEBUG = False
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

#创建应用(create our little application)
app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

#初始化数据库
# def init_db():
#     with closing(connect_db()) as db:
#         with app.open_resource('schema.sql') as f:
#             print(f.read())
#             print(type(f.read()))
#             db.cursor().executescript(str(f.read())
#         db.commit()
with closing(connect_db()) as con:
    with app.open_resource('schema.sql') as f:
        content=str(f.read())
        content=content.lstrip('b')
        content=content.replace("\'","")
        content=content.replace("\\r","")
        content=content.replace("\\n","")
        # print(content)
        cur=con.cursor()
        cur.executescript(content)
        fetchall=cur.fetchall()
        print(fetchall)
    con.commit()

