#基于flask-sqlalchemy的图书借阅系统的实现
# 这段代码是基于flask-sqlalchemy的图书借阅系统的实现，这里有两个坑，网上说的未必都对。

# 第一个是# Error：Flask-Neither SQLALCHEMY_DATABASE_URI nor SQLALCHEMY_BINDS is set.错误

# 首先app.config中要用绝对路径

# 其次是/问题，从window拷出来是\，要改

# 最后是顺序问题，先实例化Flask对象，再进行数据库配置，再实例化db

# 第二个问题是关于自增键值的初始化问题，自增键值其实挺讨厌的，主键还好可以随时变，但外键信息要保持不变还是挺难的，在这里有个小技巧，就是在__init__的时候，对于主键值可以设置一个缺省值，如果是缺省值就让他自增好了，如果不是则直接用初始化数据写死。

# 第三个问题，到底是用业务主键还是逻辑主键（rowid,自增值）的问题，这个其实很难有答案，各有各的利弊，在这里两种混合使用了，比如图书ISBN号是唯一的，就用了ISBN号做业务主键，代价是如果ISBN号录入错了，就需要调整两次才能确保数据是OK的；像借阅者和作者用的是逻辑主键（自增值），这样的代价是作者会重复，为什么不用身份证呢？实际上也是可以的，但是身份证太过于敏感了，这样的代价是要在身份证号码上加一个唯一索引，而且作者也未必有身份证，所以最终选了逻辑主键，当然像图书借阅信息，用户登陆日志，用逻辑主键就OK了。

# 第四个问题，是多对多连接用dt.table好，还是model好，也是无解的，为啥，网上可查的资源太少了，一般倾向于用dt.table，但对于dt.table的了解太少了，除非阅读源代码。

# 第五个问题，全部用ORM可行吗？估计比较悬，ORM会存在性能问题，构造复杂的SQL也够呛，所幸这里用到的暂时都比较简单，走一步算一步吧，估计会结合SQL一起用。

# 第六个问题，其实不是问题，而是一个小技巧，[dict(zip(bookinfoname, list)) for list in bookinfolist]，把字段名和原始数据构造成了一个字典列表用于初始化数据，不至于看起来太傻。

from flask import Flask
from flask_sqlalchemy import SQLAlchemy#flask中一般使用flask-sqlalchemy来操作数据库，使用起来比较简单，易于操作。
 
import os
from datetime import datetime
 
basedir = os.path.abspath(os.path.dirname(__file__))
 
app = Flask(__name__)

'''配置数据库，使flask项目和数据库相连'''
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test4.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Error：Flask-Neither SQLALCHEMY_DATABASE_URI nor SQLALCHEMY_BINDS is set.
'''实例化数据库对象'''
db = SQLAlchemy(app)


class AuthorInfo(db.Model):
    '''
    创建模型
    params:
        __tablename__   数据库名称
        authorid等      字段名
        Integer等       字段类型
    '''
    __tablename__ = "authorinfo"
    authorid = db.Column(db.Integer, primary_key=True)
    authorname = db.Column(db.String(20), nullable=False)
    authorcard = db.Column(db.String(20))
    authornationality = db.Column(db.String(20))
    # relate_bookauthor = db.relationship('BookAuthorInfo', backref=db.backref('authorinfo', lazy='dynamic'))
    def __init__(self, authorname, authorcard, authornationality, authorid=0):
        self.authorname = authorname
        self.authorcard = authorcard
        self.authornationality = authornationality
        if authorid != 0:
            self.authorid = authorid
 
    #__repr__() 方法是类的实例化对象用来做“自我介绍”的方法，默认情况下，它会返回当前对象的“类名+object at+内存地址”，而如果对该方法进行重写，可以为其制作自定义的自我描述信息。
    def __repr__(self):
        return '<author %r>' % self.authorname

class BookInfo(db.Model):
    __tablename__ = "bookinfo"
    isbnno = db.Column(db.String(20), primary_key=True)
    bookname = db.Column(db.String(50), nullable=False)
    publisher = db.Column(db.String(50))
    publicationdate = db.Column(db.String(20))
    booktype = db.Column(db.String(20))
    stockdate = db.Column(db.Date)
 
    # relate_bookauthor = db.relationship('BookAuthorInfo', backref=db.backref('bookinfo', lazy='dynamic'))
    def __init__(self, isbnno, bookname, publisher, publicationdate, booktype, stockdate):
        self.isbnno = isbnno
        self.bookname = bookname
        self.publisher = publisher
        self.publicationdate = publicationdate
        self.booktype = booktype
        self.stockdate = stockdate
 
    def __repr__(self):
        return '<book %r>' % self.isbnno
 
 
class BookStockInfo(db.Model):
    __tablename__ = "bookstockinfo"
    isbnno = db.Column(db.String(20), db.ForeignKey('bookinfo.isbnno'), primary_key=True)
    purchasenum = db.Column(db.Integer, nullable=False)
    stocknum = db.Column(db.Integer, nullable=False)
    # 后面追加
    # 其中realtionship描述了BookStockInfo和BookInfo的关系。
    # 第一个参数为对应参照的类"BookInfo"
    # 第二个参数backref为类BookStockInfo申明新属性的方法
    # 第三个参数lazy决定了什么时候SQLALchemy从数据库中加载数据
    relate_book = db.relationship('BookInfo', backref=db.backref('bookstockinfo', lazy='dynamic'))
 
    def __init__(self, isbnno, purchasenum, stocknum):
        self.isbnno = isbnno
        self.purchasenum = purchasenum
        self.stocknum = stocknum
 
    def __repr__(self):
        return '<book %r>' % self.isbnno
 
 
BookAuthor = db.Table('bookauthor',
                      db.Column('bookauthorid', db.Integer, primary_key=True),
                      db.Column('isbnno', db.String(20), db.ForeignKey('bookinfo.isbnno'), nullable=False),
                      db.Column('authorid', db.Integer, db.ForeignKey('authorinfo.authorid'), nullable=False))
 
 
class BookAuthorinfo(db.Model):
    __tablename__ = "bookauthorinfo1"
    bookauthorid = db.Column(db.Integer, primary_key=True)
    isbnno = db.Column(db.String(20), db.ForeignKey('bookinfo.isbnno'), nullable=False)
    authorid = db.Column(db.Integer, db.ForeignKey('authorinfo.authorid'), nullable=False)
    relate_book = db.relationship('BookInfo', backref=db.backref('bookauthorinfo1', lazy='dynamic'))
    relate_author = db.relationship('AuthorInfo', backref=db.backref('bookauthorinfo1', lazy='dynamic'))
 
    def __init__(self, isbnno, authorid, bookauthorid=0):
        self.isbnno = isbnno
        self.authorid = authorid
        if bookauthorid != 0:
            self.bookauthorid = bookauthorid
 
    def __repr__(self):
        return '<book %r>' % self.isbnno
 
 
class BorrowerInfo(db.Model):
    __tablename__ = "borrowerinfo"
    borrowerid = db.Column(db.Integer, primary_key=True)
    borrowername = db.Column(db.String(20), nullable=False)
    sex = db.Column(db.String(2))
    birthday = db.Column(db.Date)
    postcard = db.Column(db.String(20))
    address = db.Column(db.String(50))
    telephone = db.Column(db.String(20))
    registerdate = db.Column(db.Date)
 
    def __init__(self, borrowername, sex, birthday, postcard, address, telephone, registerdate, borrowerid=0):
        self.borrowername = borrowername
        self.sex = sex
        self.birthday = birthday
        self.postcard = postcard
        self.address = address
        self.telephone = telephone
        self.registerdate = registerdate
        if borrowerid != 0:
            self.borrowerid = borrowerid
 
    def __repr__(self):
        return '<borrower name %r>' % self.borrowername
 
 
class BorrowerPasswordInfo(db.Model):
    __tablename__ = "borrowerpasswordinfo"
    borrowerid = db.Column(db.Integer, db.ForeignKey('borrowerinfo.borrowerid'), primary_key=True)
    password = db.Column(db.String(20), nullable=False)
    relate_borrower = db.relationship('BorrowerInfo', backref=db.backref('borrowerpasswordinfo', lazy='dynamic'))
 
    def __init__(self, borrowerid, password):
        self.borrowerid = borrowerid
        self.password = password
 
    def __repr__(self):
        return '<borrower name %r>' % self.borrowername
 
 
class BorrowerLoginInfo(db.Model):
    __tablename__ = "borrowerlogininfo"
    borrowerloginid = db.Column(db.Integer, primary_key=True)
    borrowerid = db.Column(db.Integer, db.ForeignKey('borrowerinfo.borrowerid'))
    logindatetime = db.Column(db.DateTime, nullable=False)
    logoutdatetime = db.Column(db.DateTime)
    relate_borrower = db.relationship('BorrowerInfo', backref=db.backref('borrowerlogininfo', lazy='dynamic'))
 
    def __init__(self, borrowerid, logindatetime, logoutdatetime, borrowerloginid=0):
        self.borrowerid = borrowerid
        self.logindatetime = logindatetime
        self.logoutdatetime = logoutdatetime
        if borrowerloginid != 0:
            self.borrowerloginid = borrowerloginid
 
    def __repr__(self):
        return '<borrower name %r>' % self.borrowername
 
 
class BorrowerBook(db.Model):
    __tablename__ = "borrowerbook"
    borrowbookid = db.Column(db.Integer, primary_key=True)
    borrowerid = db.Column(db.Integer, db.ForeignKey('borrowerinfo.borrowerid'), nullable=False)
    isbnno = db.Column(db.String(20), db.ForeignKey('bookinfo.isbnno'), nullable=False)
    borrowdate = db.Column(db.Date)
    returndate = db.Column(db.Date)
    returnflag = db.Column(db.String(2))
    relate_borrower = db.relationship('BorrowerInfo', backref=db.backref('borrowerbook', lazy='dynamic'))
    relate_book = db.relationship('BookInfo', backref=db.backref('borrowerbook', lazy='dynamic'))
 
    def __init__(self, borrowerid, isbnno, borrowdate, returndate, returnflag='0', borrowbookid=0):
        self.borrowerid = borrowerid
        self.isbnno = isbnno
        self.borrowdate = borrowdate
        self.returnflag = returnflag
        if returndate != '':
            self.returndate = returndate
        if borrowbookid != 0:
            self.borrowbookid = borrowbookid
 
    def __repr__(self):
        return '<borrower name %r isbnno %r >' % self.borrowername, self.borrowername
 
 
if __name__ == '__main__':
 
    #删除数据库
    db.drop_all()
    #创建数据库
    db.create_all()

    '''
    INSERT方法一
    '''
    author = AuthorInfo('巴里', '', '美国')
    db.session.add(author)
    author = AuthorInfo('白鳝', '', '中国')
    db.session.add(author)
    db.session.commit()
    
    for author in AuthorInfo.query.all():
        print(author.authorid, author.authorname, author.authorcard, author.authornationality)

    '''
    INSERT方法二：批量
    '''
    bookinfolist = [['ISBN0001', '可爱的Python', '2009', '电子工业出版社', '图书', '2021-07-01'],
                    ['ISBN0002', 'Python绝技', '2018', '电子工业出版社', '图书', '2021-07-01'],
    ['ISBN0022', 'IT项目管理那些事儿', '2009', '电子工业出版社', '图书', '2021-07-01']]
    bookinfoname = ['isbnno', 'bookname', 'ublisher', 'publicationdate', 'booktype', 'stockdate']
    # bookinfodictlist=[]
    # for bookinfo in bookinfolist:
    #     bookinfodictlist.append(dict(zip(bookinfoname,bookinfo)))
    bookinfodictlist = [dict(zip(bookinfoname, list)) for list in bookinfolist]

    bookobjlist = []
    for i in bookinfodictlist:
        isbnno, bookname, publisher, publicationdate, booktype, stockdate = i.values()
        bookobj = BookInfo(isbnno=isbnno, bookname=bookname, publisher=publisher,
                            publicationdate=publicationdate, booktype=booktype,
                            stockdate=datetime.strptime(stockdate, '%Y-%m-%d'))
        bookobjlist.append(bookobj)

    db.session.add_all(bookobjlist)
    db.session.commit()

    for book in BookInfo.query.all():
        print(book.isbnno, book.bookname, book.publisher, book.publicationdate, book.booktype, book.stockdate)

    print('------------------Book Stock Process-------------------')
    bookstockinfolist = [['ISBN0001', 2, 2],
                            ['ISBN0002', 2, 2],
                            ['ISBN0022', 2, 2]]
    bookstockinfoname = ['isbnno', 'purchasenum', 'stocknum']

    bookstockinfodictlist = [dict(zip(bookstockinfoname, list)) for list in bookstockinfolist]

    bookstockobjlist = []
    for i in bookstockinfodictlist:
        isbnno, purchasenum, stocknum = i.values()
        bookstockobj = BookStockInfo(isbnno=isbnno, purchasenum=purchasenum, stocknum=stocknum)
        bookstockobjlist.append(bookstockobj)

    db.session.add_all(bookstockobjlist)
    db.session.commit()

    for bookstock in BookStockInfo.query.all():
        print(bookstock.isbnno, bookstock.purchasenum, bookstock.stocknum)

    # db.relationship应用
    # 查询isbnno == 'ISBN0008'的库存，返回BookStockInfo对象值
    # 可relate_book当做为BookStockInfo的属性，直接返回BookInfo对象
    bookstockquery = BookStockInfo.query.filter(BookStockInfo.isbnno == 'ISBN0008').first()
    # bookstockquery.purchasenum  = 2
    # bookstockquery.relate_book.bookname  ='PYTHON技术手册'
    bookauthorlist = [['ISBN0001', 23],
                        ['ISBN0002', 24],
    ['ISBN0019', 15]]
    
    bookauthorinfoname = ['isbnno', 'authorid']

    bookauthorinfodictlist = [dict(zip(bookauthorinfoname, list)) for list in bookauthorlist]

    bookauthorobjlist = []
    for i in bookauthorinfodictlist:
        isbnno, authorid = i.values()
        bookauthorobj = BookAuthorinfo(isbnno=isbnno, authorid=authorid)
        bookauthorobjlist.append(bookauthorobj)

    db.session.add_all(bookauthorobjlist)
    db.session.commit()

    for bookauthor in BookAuthorinfo.query.all():
        print(bookauthor.bookauthorid, bookauthor.isbnno, bookauthor.authorid)

    # borrowid,borrowername,sex,birthday,postcard,address,telephone,registerdate
    borrowerinfolist = [[1, '张三', '男', '2000-01-01', '400111200001010043', '海口市', '13800100001', '2021-09-01'],
                        [4, '赵六', '女', '1989-10-11', '400111198910110041', '海口市', '13800600002', '2021-09-03']]
    borrowerinfoname = ['borrowid', 'borrowername', 'sex', 'birthday', 'postcard', 'address', 'telephone',
                        'registerdate']
    borrowerinfodictlist = [dict(zip(borrowerinfoname, list)) for list in borrowerinfolist]

    borrowerobjlist = []
    for i in borrowerinfodictlist:
        borrowerid, borrowername, sex, birthday, postcard, address, telephone, registerdate = i.values()
        borrowerrbj = BorrowerInfo(borrowername=borrowername, sex=sex, birthday=datetime.strptime(birthday, '%Y-%m-%d'),
                                    postcard=postcard,
                                    address=address, telephone=telephone,
                                    registerdate=datetime.strptime(registerdate, '%Y-%m-%d'), borrowerid=borrowerid)
        borrowerobjlist.append(borrowerrbj)

    db.session.add_all(borrowerobjlist)
    db.session.commit()

    for borrowerinfo in BorrowerInfo.query.all():
        print(borrowerinfo.borrowername, borrowerinfo.sex, borrowerinfo.birthday, borrowerinfo.postcard,
                borrowerinfo.address, borrowerinfo.telephone, borrowerinfo.registerdate, borrowerinfo.borrowerid)

    borrowerpasswordlist = [[1, '1qaz!QAZ'],
                            [4, '1qaz!QAZ']]
    borrowerpasswordname = ['borrowerid', 'password']
    borrowerpassworddictlist = [dict(zip(borrowerpasswordname, list)) for list in borrowerpasswordlist]

    borrowerpasswordobjlist = []
    for i in borrowerpassworddictlist:
        borrowerid, password = i.values()
        borrowerpasswordobj = BorrowerPasswordInfo(borrowerid=borrowerid, password=password)
        borrowerpasswordobjlist.append(borrowerpasswordobj)

    db.session.add_all(borrowerpasswordobjlist)
    db.session.commit()

    for borrowerpasswordinfo in BorrowerPasswordInfo.query.all():
        print(borrowerpasswordinfo.borrowerid, borrowerpasswordinfo.password)

    borrowerloginlist = [[1, '2021-09-01 10:01:00', '2021-09-01 12:01:00', 1],
                            [1, '2021-09-03 10:01:00', '2021-09-03 12:01:00', 5]]
    borrowerloginname = ['borrowerid', 'logindatetime', 'logoutdatetime', 'borrowerloginid']
    borrowerlogindictlist = [dict(zip(borrowerloginname, list)) for list in borrowerloginlist]

    borrowerloginobjlist = []
    for i in borrowerlogindictlist:
        borrowerid, logindatetime, logoutdatetime, borrowerloginid = i.values()
        borrowerloginobj = BorrowerLoginInfo(borrowerid=borrowerid,
                                                logindatetime=datetime.strptime(logindatetime, '%Y-%m-%d %H:%M:%S'),
                                                logoutdatetime=datetime.strptime(logoutdatetime, '%Y-%m-%d %H:%M:%S'),
                                                borrowerloginid=borrowerloginid)
        borrowerloginobjlist.append(borrowerloginobj)

    db.session.add_all(borrowerloginobjlist)
    db.session.commit()

    for borrowerlogininfo in BorrowerLoginInfo.query.all():
        print(borrowerlogininfo.borrowerid, borrowerlogininfo.logindatetime, borrowerlogininfo.logoutdatetime,
                borrowerlogininfo.borrowerloginid)

    borrowerbooklist = [[1, 'ISBN0001', '2021-09-01', '2021-09-02', '1', 1],
                        [1, 'ISBN0005', '2021-09-03', '', '0', 6]]
    borrowerbookname = ['borrowerid', 'isbnno', 'borrowdate', 'returndate', 'returnflag', 'borrowbookid']
    borrowerbookdictlist = [dict(zip(borrowerbookname, list)) for list in borrowerbooklist]

    borrowerbookobjlist = []
    for i in borrowerbookdictlist:
        borrowerid, isbnno, borrowdate, returndate, returnflag, borrowbookid = i.values()
        if returndate != '':
            returndate = datetime.strptime(returndate, '%Y-%m-%d')
        borrowerbookobj = BorrowerBook(borrowerid=borrowerid,
                                        isbnno=isbnno,
                                        borrowdate=datetime.strptime(borrowdate, '%Y-%m-%d'),
                                        returndate=returndate,
                                        returnflag=returnflag,
                                        borrowbookid=borrowbookid)
        borrowerbookobjlist.append(borrowerbookobj)

    db.session.add_all(borrowerbookobjlist)
    db.session.commit()

    for borrowerbookinfo in BorrowerBook.query.all():
        print(borrowerbookinfo.borrowerid, borrowerbookinfo.isbnno, borrowerbookinfo.borrowdate,
                borrowerbookinfo.returndate, borrowerbookinfo.returnflag, borrowerbookinfo.borrowbookid)