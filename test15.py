#用Python进行SQLite数据库操作
import sqlite3

#创建数据库
con=sqlite3.connect('templates/flaskr.db')
#游标对象是用来执行select查询数据库的，db连接对象才是用来做增删改操作的
cur=con.cursor()

#创建表格
try:
    cur.execute('create table region(id interger primary key,name varchar(10))')
except sqlite3.OperationalError as e:
    print('表格region已存在')
#插入一条数据
try:
    cur.execute('insert into region(id,name) values("7","杭州")')
except sqlite3.IntegrityError as e:
    print('单条id已存在')
#插入多条记录
try:
    regions=[("5","上海"),["6","北京"]]
    for region in regions:
        cur.execute("insert into region(id,name) values(?,?)",region)
except sqlite3.IntegrityError as e:
    print('多条id已存在')

#查询数据
cur.execute("select * from region")
print(cur.execute("select * from region"))
# print(cur.fetchall())

fetchall=cur.fetchall()
print(fetchall)
for item in fetchall:
    for element in item:
        print(element)
#提交数据库
con.commit()
con.close()