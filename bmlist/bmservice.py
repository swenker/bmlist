#! /usr/bin/env python
#coding=utf-8
"""
list all of the books of a given user
"""
import hashlib
import decimal
from datetime import datetime
from entities  import User,Book
import web

from bookparser import BookParser
from savedbookparser import SavedBookParser
from serviceconfig import *
from bmlistexceptions import *

TABLE_USERBOOK="bm_user_book"
TABLE_BOOK="bm_book"
TABLE_USER="bm_user"
STATUS_DELETE=0
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'



logger=bmconfig.getlogger("BmService")

db = web.database(dbn=bmconfig.dbn,db=bmconfig.db,host=bmconfig.host,user=bmconfig.user,passwd=bmconfig.passwd,charset='utf8')
decimal.getcontext().prec=2

class AccountService():

    def signin(self,email,passwd):
        email = email.lower()
        passwd=tomd5(passwd)
        result = db.select(TABLE_USER,where='email=$email',vars=locals())
        if result:
            r=result[0]
            user = User()
            user.email=r['email']
            user.nickname=r['nickname']
            user.cellphone=r['cellphone']
            user.status = r['status']

            pwindb=r['passwd']
            #TODO compare char by char?
            if pwindb == passwd:
                return user

        return None

    def signup(self,user):
        """new user"""
        passwd=tomd5(user.passwd)
        if not self.exists(user.email):
            sqls = "INSERT INTO %s(email,passwd,nickname,cellphone,create_time) VALUES(%s,%s,%s,%s,%s)" \
                  %(TABLE_USER,user.email,passwd,user.nickname,user.cellphone,datetime.now().strftime(TIME_FORMAT))
            result = db.query(sqls)
        else:
            msg="email:%s already exist."%(user.email)
            logger.info(msg)
            raise ObjectExistsException(msg)

    def exists(self,email):
        email = email.lower()
        result = db.select(TABLE_USER,where='email=$email',vars=locals())
        if result:
            return len(result)>0
        return False

    def delete(self,uid):
        db.delete(TABLE_USER,where="uid=$uid",vars=locals())

    def changePasswd(self,uid,oldpwd,newpwd):
        raise NotImplementedException("Not Implemented")

class BookService(object):

    def __init__(self):
        self.bookParser = BookParser()

    def list_user_books(self,uid,start,end):
        """list the books of a given user by uid"""

        sqls="SELECT a.bid,isbn10,isbn13,title,subtitle,author,translators,publisher,pubdate,price,pages,update_time,create_time,quantity,\
                       series,keywords,summary,b.status \
                       FROM "+TABLE_USERBOOK+" a RIGHT JOIN "+TABLE_BOOK+" b ON a.bid=b.bid WHERE a.uid=%d " % uid

        if end:
            sqls+= " LIMIT %d,%d" % (start,end)

        logger.debug(sqls)
        result= db.query(sqls)
        
        books=[]

        if result:
            for r in result:
                book  = self.compose_book(r)
                books.append(book)

        return books

    def list_books(self,start,nfetch,query_in_title=None):
        """list the books """
        sqlc="SELECT COUNT(*) as total FROM bm_book "
        sqls="SELECT bid,isbn10,isbn13,title,subtitle,author,translators,publisher,pubdate,price,pages,update_time,create_time,quantity,\
                       series,keywords,summary,status \
                       FROM "+TABLE_BOOK

        if query_in_title:
            sqlwhere=" WHERE title LIKE '%"+query_in_title+"%' OR author LIKE '%"+query_in_title+"%'"
            sqls+=sqlwhere
            sqlc +=sqlwhere

        sqls +=" ORDER BY title,author "


        sqls+=" LIMIT %d,%d" % (start,nfetch)

        logger.debug(sqls)

        total=0
        result=db.query(sqlc)
        if result:
            for r in result:
                total = r['total']

        result = db.query(sqls)

        books=[]
        if result:
            for r in result:
                book=self.compose_book(r)

                books.append(book)

        return books,total
        
    def compose_book(self,r):

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
        book.transtr = book._transtr()
        return book


    def get_book_byisbn_fromremote(self,isbn):
        return self.bookParser.parsebookbyisbn(isbn)

    def insert_book(self,isbn,uid=None):
        """get book by isbn from douban and insert it into local db"""
        try:
            if not uid:
                uid=1
            book = self.get_book_byisbn(isbn)
            if book and book.id:
                #check if it's already in user book list?
                sqls="select 1 FROM %s WHERE `uid`=%d and `bid`=%d" %(TABLE_USERBOOK,uid,book.id)

                result=db.query(sqls)

                if result:
                    logger.debug(("already exist:",isbn))
                    return 
                else:
                    self.add_userbook(uid,book.id)
            else:
                book = self.get_book_byisbn_fromremote(isbn)
                
                if book :
                    t=db.transaction()
                    bid = self.create_book(book)
                    if bid:
                        self.add_userbook(uid,bid)
                    else:
                        logger.warn(('failed to get bid:', bid))
                    t.commit()
                else:
                    logger.warn(('book not returned:%s' % isbn))
        except Exception,e:
            logger.error(e)

          
    def get_book_byisbn(self,isbn):
        isbn_column=''
        isbn=isbn.strip()
        if len(isbn) == 10:
            isbn_column='isbn10'
        else:
            isbn_column='isbn13'

        sqls = "SELECT  bid,isbn10,isbn13,title,subtitle,author,translators,publisher,pubdate,price,pages,update_time,create_time,quantity,\
        series,keywords,summary,status FROM %s WHERE %s = '%s'" %(TABLE_BOOK,isbn_column,isbn)

        logger.debug(sqls)
        result=db.query(sqls)

        book = None
        if result:
            book  = self.compose_book(result[0])

        return book

    def get_book_byid(self,bid):

        book = None
        if bid:
            sqls = "SELECT bid,isbn10,isbn13,title,subtitle,author,translators,publisher,pubdate,price,pages,update_time,create_time,quantity,\
            series,keywords,summary,status FROM %s WHERE bid = %s" %(TABLE_BOOK,bid)

            logger.debug(sqls)
            result = db.query(sqls)

            if result:
                book  = self.compose_book(result[0])

        return book


    def create_book(self,book):

        if book and book.id:
            logger.warn("should go to update...")
            return
        #sqls="INSERT INTO %s(isbn10,isbn13,title,subtitle,author,translators,publisher,pubdate,price,pages,create_time,quantity,\
        #series,keywords,summary)values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%d','%s','%d','%s','%s','%s')" \
        #%(TABLE_BOOK,book.isbn10,book.isbn13,book.title,book.subtitle,book.author,";".join(book.translators),book.publisher,book.pubdate,\
        #book.price,book.pages,datetime.now().strftime(TIME_FORMAT),book.quantity,book.series,book.keywords,book.summary)

        sqls="INSERT INTO %s(isbn10,isbn13,title,subtitle,author,translators,publisher,pubdate,price,pages,create_time,quantity,\
        series)values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%d','%s','%d','%s')" \
        %(TABLE_BOOK,book.isbn10,book.isbn13,book.title,book.subtitle,book.author,";".join(book.translators),book.publisher,book.pubdate,
        book.price,book.pages,datetime.now().strftime(TIME_FORMAT),book.quantity,book.series)

        #print sqls
        logger.debug(sqls)
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

                 #TODO is it more elegant to copy title to this table?
                 sqls='DELETE FROM %s where bid=%d' % (TABLE_USERBOOK,bid)
                 db.query(sqls)

            logger.info(("book:%d was deleted:%s" %(bid,hard)))
        except Exception ,e:
            print e
            t.rollback()
        else:
            t.commit()

     
    def remove_userbook(self,uid,bid):
        """remove book from user book list"""
        sqls="DELETE FROM %s WHERE `uid`=%d and `bid`=%d" %(TABLE_USERBOOK,uid,bid)
        db.query(sqls)

    def import_book(self,datafile="booklist.xml"):
        parser = SavedBookParser()
        parser.parse_saved_book(datafile)

        isbnlist=parser.isbnlist
        logger.debug(len(isbnlist))

        isbnfailed=[]
        for isbn in isbnlist:
            #print isbn
            book = None
            try:
                book =self.get_book_byisbn_fromremote(isbn)
                self.create_book(book)
            except Exception,e:
                isbnfailed.append(isbn)
                print isbn,book,e
        logger.info("======complete======")
        logger.warn("failed:%s" % isbnfailed)
        return (len(isbnlist),isbnfailed)

    def dump_book(self):
        booklist=self.list_books(0,10000)

        xmlstr="""<?xml version="1.0" encoding="UTF-8"?>"""

        xmlstr+="<books>"

        for b in booklist:
            bstr="<book><id>%d</id><isbn10>%s</isbn10><isbn13>%s</isbn13><title>%s</title><author>%s</author><publisher>%s</publisher><pubdate>%s</pubdate><pages>%d</pages><price>%f</price></book>\n"\
                 %(b.id,b.isbn10,b.isbn13,b.title,b.author,b.publisher,b.pubdate,b.pages,b.price)

            xmlstr+=bstr

        xmlstr+="</books>"

        #print xmlstr
        xmlfile=r"D:\work\projects\111-tech-bmlist\bmfile.xml"
        with open(xmlfile,'w') as f:
            f.write(xmlstr.encode("utf-8"))
        f.close()

    def export_book(self):
        booklist=self.list_books(0,1000)

        xmlstr="""<?xml version="1.0" encoding="UTF-8"?>"""

        xmlstr+="<books>"

        for b in booklist:
            bstr="<book><id>%d</id><isbn10>%s</isbn10><isbn13>%s</isbn13><title>%s</title><author>%s</author><publisher>%s</publisher><pubdate>%s</pubdate><pages>%d</pages><price>%f</price></book>\n"\
                 %(b.id,b.isbn10,b.isbn13,b.title,b.author,b.publisher,b.pubdate,b.pages,b.price)

            xmlstr+=bstr

        xmlstr+="</books>"

        #print xmlstr
        xmlfile=r"D:\work\projects\111-tech-bmlist\bmfile.xml"
        with open(xmlfile,'w') as f:
            f.write(xmlstr.encode("utf-8"))
        f.close()

def tomd5(s):
    md5handler=hashlib.md5(s)
    return md5handler.hexdigest()

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




        
