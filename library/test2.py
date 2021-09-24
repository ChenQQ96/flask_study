#数据库设计和ORM映射


import sqlite3
import os
 
# 删除数据库
try:
    os.unlink("library/test2.db")
except:
    pass
 
# 默认创建数据库
# -----------------创建数据表-----------------
conn = sqlite3.connect('library/test2.db')
print("Opened database successfully")
c = conn.cursor()
c.execute('''CREATE TABLE COMPANY
       (ID INT PRIMARY KEY     NOT NULL,
       NAME           TEXT    NOT NULL,
       AGE            INT     NOT NULL,
       ADDRESS        CHAR(50),
       SALARY         REAL);''')
print("Table created successfully")
conn.commit()
conn.close()
 
# -----------------insert插入语句-----------------
conn = sqlite3.connect('library/test2.db')
c = conn.cursor()
print("Opened database successfully")
c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY)  VALUES (1,'Paul', 32,'California', 20000.00 )")
c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) VALUES (2,'Allen', 25,'Texas', 15000.00 )")
c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) VALUES (3,'Teddy', 23,'Norway', 20000.00 )")
c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) VALUES (4,'Mark', 25,'Rich-Mond', 65000.00 )")
conn.commit()
print("Records created successfully")
conn.close()
 
# -----------------select查询语句-----------------
conn = sqlite3.connect('library/test2.db')
c = conn.cursor()
cursor = c.execute("SELECT id, name, address, salary  from COMPANY")
for row in cursor:
    print("ID = ", row[0])
    print("NAME = ", row[1])
    print("ADDRESS = ", row[2])
    print("SALARY = ", row[3], "\n")
print("Operation done successfully")
conn.close()


# -----------------update更新语句-----------------
conn = sqlite3.connect('library/test2.db')
c = conn.cursor()
c.execute("UPDATE COMPANY set SALARY = 25000.00 where ID=1")
conn.commit()
print("Total number of rows updated :", conn.total_changes)
 
cursor = conn.execute("SELECT id, name, address, salary  from COMPANY")
for row in cursor:
    print("ID = ", row[0])
    print("NAME = ", row[1])
    print("ADDRESS = ", row[2])
    print("SALARY = ", row[3], "\n")
print("Operation done successfully")

# -----------------delete删除语句-----------------
conn = sqlite3.connect('library/test2.db')
c = conn.cursor()
c.execute("DELETE from COMPANY where ID=2;")
conn.commit()
print("Total number of rows deleted :", conn.total_changes)
 
cursor = conn.execute("SELECT id, name, address, salary  from COMPANY")
for row in cursor:
    print("ID = ", row[0])
    print("NAME = ", row[1])
    print("ADDRESS = ", row[2])
    print("SALARY = ", row[3], "\n")
print("Operation done successfully")
conn.close()
