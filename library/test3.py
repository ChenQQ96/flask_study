#数据库设计和ORM映射
#根据教程中的表格，创建数据表

import sqlite3
import os
db='library/test3.db'
# 删除数据库
os.unlink(db)

# 默认创建数据库
# -----------------创建数据表-----------------
conn = sqlite3.connect(db)
print("Opened database successfully")
c = conn.cursor()

authorinfotable = '''
create table authorinfo(
        authorid   INTEGER    PRIMARY KEY    ,
        authorname varchar(20)       NOT NULL,
        authorcard varchar(20)       ,
        authornationality  varchar(20)
);'''
bookinfotable = '''
create table bookinfo(
        isbnno varchar(20)    PRIMARY KEY    NOT NULL,
        bookname   varchar(50)       NOT NULL,
        publisher  varchar(50)       ,
        publicationdate    varchar(20)       ,
        booktype   varchar(20)       ,
        stockdate  date      NOT NULL,
        FOREIGN KEY(isbnno) REFERENCES bookinfo(isbnno)
);'''
bookstockinfotable = '''
create table bookstockinfo(
        isbnno varchar(20)    PRIMARY KEY    NOT NULL,
        purchasenum    int       NOT NULL,
        stocknum   int       NOT NULL
);'''
bookauthorinfotable = '''
create table bookauthorinfo(
        bookauthorid   INTEGER    PRIMARY KEY    NOT NULL,
        isbnno varchar(20)       NOT NULL,
        authorid   int       NOT NULL,
        FOREIGN KEY(isbnno) REFERENCES bookinfo(isbnno),
        FOREIGN KEY(authorid) REFERENCES authorinfo(authorid)
);'''
borrowerinfotable = '''
create table borrowerinfo  (
        borrowid   INTEGER    PRIMARY KEY    NOT NULL,
        borrowername   varchar(20)       NOT NULL,
        sex    varchar(2)    ,
        birthday   date      ,
        postcard   varchar(20)       ,
        address    varchar(50)       ,
        telephone  varchar(20)       ,
        registerdate   date      NOT NULL
);'''
borrowerpasswordinfotable = '''
create table borrowerpasswordinfo(
        borrowid   INTEGER    PRIMARY KEY    NOT NULL,
        password   varchar(20)       NOT NULL
);'''
borrowerlogintable = '''
create table borrowerlogin(
        borrowerloginid    INTEGER    PRIMARY KEY    NOT NULL,
        borrowid   int       NOT NULL,
        logindatetime  datetime      NOT NULL,
        logoutdatetime datetime      ,
        FOREIGN KEY(borrowid) REFERENCES borrowerinfo(borrowid)
);'''
borrowbooktable = '''
create table borrowbook(
        borrowbookid   INTEGER    PRIMARY KEY    NOT NULL,
        borrowid   int       NOT NULL,
        isbnno varchar(20)       NOT NULL,
        borrowdate date      NOT NULL,
        returndate date      ,
        returnflag char(1)       ,
        FOREIGN KEY(borrowid) REFERENCES borrowerinfo(borrowid),
        FOREIGN KEY(isbnno) REFERENCES bookinfo(isbnno)
);'''
c.execute(bookinfotable)
print("bookinfotable created successfully")
c.execute(bookstockinfotable)
print("bookstockinfotable created successfully")
c.execute(bookauthorinfotable)
print("bookauthorinfotable created successfully")
c.execute(authorinfotable)
print("authorinfotable created successfully")
c.execute(borrowerinfotable)
print("borrowerinfotable created successfully")
c.execute(borrowerpasswordinfotable)
print("borrowerpasswordinfotable created successfully")
c.execute(borrowerlogintable)
print("borrowerlogintable created successfully")
c.execute(borrowbooktable)
print("borrowbooktable created successfully")
conn.commit()
conn.close()

# -----------------插入数据-----------------
conn = sqlite3.connect(db)
c = conn.cursor()
print("Opened database successfully")
c.execute("INSERT INTO authorinfo (authorid,authorname,authorcard,authornationality)  VALUES (1,'巴里','' ,'美国')")
c.execute("INSERT INTO authorinfo (authorid,authorname,authorcard,authornationality)  VALUES (2,'白鳝','' ,'中国')")

conn.commit()
print( "authorinfo Records created successfully")

c.execute( "INSERT INTO bookinfo VALUES ('ISBN0001','可爱的Python','2009','电子工业出版社','图书','2021-07-01')")
c.execute( "INSERT INTO bookinfo VALUES ('ISBN0002','Python绝技','2018','电子工业出版社','图书','2021-07-01')")
conn.commit()


c.execute( "INSERT INTO bookstockinfo VALUES ('ISBN0001',2,2)")
c.execute( "INSERT INTO bookstockinfo VALUES ('ISBN0002',2,2)")
conn.commit()
 
c.execute("INSERT INTO bookauthorinfo(isbnno,authorid)  VALUES ('ISBN0001',23)")
conn.commit()
 
c.execute(
    "INSERT INTO borrowerinfo  VALUES (1,'张三','男','2000-01-01','400111200001010043','海口市','13800100001','2021-09-01')")
c.execute(
    "INSERT INTO borrowerinfo  VALUES (2,'李四','男','1982-10-01','400111198210010041','海口市','13800300002','2021-09-01')")

conn.commit()
 
c.execute("INSERT INTO borrowerpasswordinfo  VALUES (1,'1qaz!QAZ')")
conn.commit()
 
c.execute("INSERT INTO borrowerlogin  VALUES (1,1,'2021-9-1 10:01','2021-9-1 12:01')")
conn.commit()
 
c.execute("INSERT INTO borrowbook  VALUES (1,1,'ISBN0001','2021-09-01','2021-09-02','1')")

conn.commit()
 
conn.close()

# -----------------查询数据-----------------
conn = sqlite3.connect(db)
c = conn.cursor()
print("Opened database successfully")
cursor = c.execute("SELECT authorid,authorname,authorcard,authornationality  from authorinfo")
for row in cursor:
    print(row)
cursor = c.execute("SELECT *  from bookinfo")
for row in cursor:
    print(row)
cursor = c.execute("SELECT *  from bookstockinfo")
for row in cursor:
    print(row)
cursor = c.execute("SELECT *  from bookauthorinfo")
for row in cursor:
    print(row)
cursor = c.execute("SELECT *  from borrowerinfo")
for row in cursor:
    print(row)
cursor = c.execute("SELECT *  from borrowerpasswordinfo")
for row in cursor:
    print(row)
cursor = c.execute("SELECT *  from borrowerlogin")
for row in cursor:
    print(row)
cursor = c.execute("SELECT *  from borrowbook")
for row in cursor:
    print(row)
print("Operation done successfully")
conn.close()