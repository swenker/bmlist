#! /usr/bin/env python
#coding=utf-8
"""
list all of the books of a given user
"""
import hashlib
from datetime import datetime
from entities  import User,Book
from bookparser import BookParser
import web
from savedbookparser import SavedBookParser
from ConfigParser import ConfigParser
import decimal

TABLE_USERBOOK="bm_user_book"
TABLE_BOOK="bm_book"
TABLE_USER="bm_user"
STATUS_DELETE=0
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'


class BmConfig():
    def __init__(self):
        configparser=ConfigParser()
        configparser.read("bmlist.cfg")
        self.dbn=configparser.get('db','dbn','mysql')
        self.host=configparser.get('db','host','mysql')
        self.db=configparser.get('db','db','bmlist')
        self.user=configparser.get('db','user','bmlist')
        self.passwd=configparser.get('db','passwd','bmlist1')

bmconfig = BmConfig()
db = web.database(dbn=bmconfig.dbn,db=bmconfig.db,host=bmconfig.host,user=bmconfig.user,passwd=bmconfig.passwd,charset='utf8')
decimal.getcontext().prec=2

class UserService():

    def checkuser(self,email,passwd):
        passwd=self.tomd5(passwd)
        result = db.select(TABLE_USER,where='email=$email and passwd=$passwd',vars=locals())
        if (result):
            r=result[0]
            user = User()
            user.email=r['email']
            user.nickname=r['nickname']
            user.cellphone=r['cellphone']
            user.status = r['status']

            return user

        return None

    def tomd5(s):
        md5handler=hashlib.md5(s)
        return md5handler.hexdigest()


class BookService(object):

    def __init__(self):
        #self.connection = None
        self.bookParser = BookParser()

    def list_user_books(self,uid,start,end):
        "list the books of a given user by uid"

        sqls="select a.bid,isbn10,isbn13,title,subtitle,author,translators,publisher,pubdate,price,pages,update_time,create_time,quantity,\
                       series,keywords,summary,b.status \
                       from "+TABLE_USERBOOK+" a right join "+TABLE_BOOK+" b on a.bid=b.bid where a.uid=%d" %(uid)

        if end>1:
            sqls+= "limit %d,%d" % (start,end)
        result= db.query(sqls)
        
        books=[]

        if result:
            for r in result:

                book  = self.composebook(r)
                books.append(book)

        return books

    def list_books(self,start,end):
        "list the books "
        sqls="select bid,isbn10,isbn13,title,subtitle,author,translators,publisher,pubdate,price,pages,update_time,create_time,quantity,\
                       series,keywords,summary,status \
                       from "+TABLE_BOOK
        if end>1:
               sqls+=" limit %d,%d" % (start,end)

        result = db.query(sqls)

        books=[]
        if result:
            for r in result:
                book=self.composebook(r)

                books.append(book)

        return books
        
    def composebook(self,r):

        book  = Book()
        book.id = r['bid']
        book.isbn10 = r['isbn10']
        book.isbn13 = r['isbn13']
        book.title = r['title']
        book.subtitle = r['subtitle']
        book.author = r['author']
        book.translators = r['translators']
        book.publisher = r['publisher']
        book.pubdate = r['pubdate']
        book.price = r['price']
        book.pages = r['pages']
        book.update_time = r['update_time']
        book.create_time = r['create_time']
        book.quantity = r['quantity']
        book.series = r['series']
        book.keywords = r['keywords']
        book.summary = r['summary']
        book.status = r['status']

        return book


    def getbookbyisbnfromremote(self,isbn):
        return self.bookParser.parsebookbyisbn(isbn)

    def insert_book(self,isbn,uid):
        "get book by isbn from douban and insert it into local db"
        try:            
            bid = self.get_book_byisbn(isbn)
            if(bid>0):
                #check if it's already in user book list?

                sqls="select 1 FROM %s WHERE `uid`=%d and `bid`=%d" %(TABLE_USERBOOK,uid,bid)
                result=db.query(sqls)

                if result:
                    print "already exist:",isbn

                    return 
                else:
                    self.add_userbook(uid,bid)
            else:
                #compose book here
                book = self.getbookbyisbnfromremote(isbn)
                
                if book :   
                    bid = self.create_book(book)
                    if(bid >0):
                        self.add_userbook(uid,bid)
                    else:
                        print 'failed to get bid:',bid
                else:
                    print 'book not returned:%s'  % isbn
        except Exception,e:
            print e

          
    def get_book_byisbn(self,isbn):

        bid=-1
        isbn_column=''
        if len(isbn) == 13:
            isbn_column='isbn13'
        else:
            isbn_column='isbn10'    

        sqls = "SELECT bid,status FROM %s WHERE %s = %s" %(TABLE_BOOK,isbn_column,isbn)
        result=db.query(sqls)

        if result:
            bid = result[0]['bid']

        return bid

    def get_book_byid(self,bid):

        sqls = "SELECT bid,isbn10,isbn13,title,subtitle,author,translators,publisher,pubdate,price,pages,update_time,create_time,quantity,\
        series,keywords,summary,status FROM %s WHERE bid = %s" %(TABLE_BOOK,bid)

        result = db.query(sqls)

        book = None
        if result:
            book  = self.composebook(result[0])

        return book


    def create_book(self,book):

        if book.id and book.id>0:
            print "should go to update..."
            return
        #sqls="INSERT INTO %s(isbn10,isbn13,title,subtitle,author,translators,publisher,pubdate,price,pages,create_time,quantity,\
        #series,keywords,summary)values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%d','%s','%d','%s','%s','%s')" \
        #%(TABLE_BOOK,book.isbn10,book.isbn13,book.title,book.subtitle,book.author,";".join(book.translators),book.publisher,book.pubdate,\
        #book.price,book.pages,datetime.now().strftime(TIME_FORMAT),book.quantity,book.series,book.keywords,book.summary)

        sqls="INSERT INTO %s(isbn10,isbn13,title,subtitle,author,translators,publisher,pubdate,price,pages,create_time,quantity,\
        series)values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%d','%s','%d','%s')" \
        %(TABLE_BOOK,book.isbn10,book.isbn13,book.title,book.subtitle,book.author,";".join(book.translators),book.publisher,book.pubdate,\
        book.price,book.pages,datetime.now().strftime(TIME_FORMAT),book.quantity,book.series)

        #print sqls
        
        db.query(sqls)
        
        result = db.query('select LAST_INSERT_ID() AS bid')
        bid=-1

        if result:
            bid = result[0]['bid']

        return bid

    def add_userbook(self,uid,bid):
        sqls="INSERT INTO %s (uid,bid,status)values('%d','%d',1)" % (TABLE_USERBOOK,uid,bid)
        db.query(sqls)

    def updatebook(self,book):
        bid=book.id
        db.update(TABLE_BOOK,where="bid=$bid",vars=locals(),isbn10=book.isbn10,isbn13=book.isbn13,title=book.title,subtitle=book.subtitle,author=book.author,translators=";".join(book.translators),
                  publisher=book.publisher,pubdate=book.pubdate,price=book.price,pages=book.pages,update_time=datetime.now().strftime(TIME_FORMAT),quantity=book.quantity,series=book.series)

    def remove_book(self,bid,hard=False):
        t=db.transaction()
        try:
            if not hard:
                sqls="UPDATE %s SET `status`=%d where bid=%d" % (TABLE_BOOK,0,bid)
                db.query(sqls)

                #TODO is it more elegant to copy title to this table?
                sqls='UPDATE %s SET `status`=%d where bid=%d' % (TABLE_USERBOOK,0,bid)
                db.query(sqls)
            else:
                 sqls="DELETE FROM %s where bid=%d" % (TABLE_BOOK,bid)
                 db.query(sqls)

                 #TODO is is more elegant to copy title to this table?
                 sqls='DELETE FROM %s where bid=%d' % (TABLE_USERBOOK,bid)
                 db.query(sqls)
        except Exception ,e:
            print e
            t.rollback()
        else:
            t.commit()

     
    def remove_userbook(self,uid,bid):
        "remove book from user book list"
        sqls="DELETE FROM %s WHERE `uid`=%d and `bid`=%d" %(TABLE_USERBOOK,uid,bid)
        db.query(sqls)

    def importbook(self):
        parser = SavedBookParser()
        file="booklist.xml"
        parser.parsesavedbook(file)

        isbnlist=parser.isbnlist
        print len(isbnlist)
        isbnfailed=[]
        for isbn in isbnlist:
            #print isbn
            book = None
            try:
                book =self.getbookbyisbnfromremote(isbn)
                self.create_book(book)
            except Exception,e:
                isbnfailed.append(isbn)
                print isbn,book,e
        print "======complete======"
        print isbnfailed

    def exportbook(self):
        booklist=self.list_books(0,1000)

        xmlstr="""<?xml version="1.0" encoding="UTF-8"?>"""

        xmlstr+="<books>"

        for b in booklist:
            bstr="<book><isbn10>%s</isbn10><isbn13>%s</isbn13><title>%s</title><author>%s</author><publisher>%s</publisher><pubdate>%s</pubdate><pages>%d</pages><price>%f</price></book>\n"\
                 %(b.isbn10,b.isbn13,b.title,b.author,b.publisher,b.pubdate,b.pages,b.price)

            xmlstr+=bstr

        xmlstr+="</books>"

        print xmlstr
        xmlfile=r"D:\work\projects\111-tech-bmlist\bmfile.xml"
        with open(xmlfile,'w') as f:
            f.write(xmlstr.encode("utf-8"))
        f.close()

def display_books(books):
    for book in books:
        print book



if __name__ == '__main__':
    print "testing"
    bookservice = BookService()
    #bookservice.insert_book('9787547012314',1)
    #bookService.remove_book(3)
    books= bookservice.list_books(0,1000)

    print len(books)
    print books[0]
    #print bookservice.list_user_books(1,0,1000)




        
