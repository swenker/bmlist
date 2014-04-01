__author__ = 'samsung'

import web
from entities import *
from bmservice import UserService,BookService
from bookparser import BookParser
from decimal import *

URL_CREATE='/bm/book/create'
urls=(
    '/bm','Home',
    '/bm/s','PrintService',
    '/bm/user/signin','UserSignin',
    '/bm/book/check','CheckBook',
    '/bm/book/list/(\d*)','ListBooks',
    '/bm/book/get/(\d+)', 'GetBook',
    '/bm/book/editform/(\d+)', 'EditBook',
    '/bm/book/edit', 'EditBook',
    URL_CREATE,'CreateBook',
    '/bm/book/delete/(\d+)','DeleteBook',
    '/bm/book/add?bid=23','AddBook'
)

app=web.application(urls,globals())
application = app.wsgifunc()

session = web.session.Session(app, web.session.DiskStore('sessions.bm'), initializer={'bmuser': None})
render = web.template.render("templates")

bookservice = BookService()

class Home():
    def GET(self):
        return render.index()

class PrintService():
    def GET(self):
        return urls


def updatesession(user):
    session.bmuser=user

def checksession(user):
    if not session.bmuser :
        session.bmuser=user
    else:

        return session.bmuser


class UserSignin():
    def GET(self):
        params = web.input(signin=None)

        if(params.signin and params.signin=='SignIn'):
            return render.signin()
        else:
            email = params.email
            passwd= params.passwd

            userservice=UserService()
            bmuser=userservice.checkuser(email,passwd)

            if bmuser:
                updatesession(bmuser)

            return "OK"


class ListBooks():
    def GET(self,uid=None):
        params = web.input(np=0)
        npages=params.np

        booklist=None
        start=0
        end=-1
        if(not uid):
            booklist = bookservice.list_books(start,end)

        else:
            booklist = bookservice.list_user_books(uid,start,end)

        return render.booklist(booklist)

class CheckBook():
    def GET(self):
        params = web.input()
        isbn = params.isbn

        bookparser = BookParser()
        book = bookparser.parsebookbyisbn(isbn)
        if(not book):
            book=Book()
        return render.bookedit(book,URL_CREATE)
        #else:
        #    return "Not Found By ISBN:"+isbn

class GetBook():
    def GET(self,bid):
        book = bookservice.get_book_byid(bid)

        return render.bookview(book)

class EditBook():
    aurl="/bm/book/edit"
    def GET(self,bid):
        book = bookservice.get_book_byid(bid)
        return render.bookedit(book,EditBook.aurl)

    def POST(self):
        params=web.input()
        bid=params.bid

        book = bookservice.get_book_byid(bid)
        book.title=params.title
        book.subtitle=params.subtitle
        book.isbn10=params.isbn10
        book.isbn13=params.isbn13
        book.author=params.author
        if(params.translators):
            book.translators = params.translators.split(";")
        #book.translators=params.translators
        book.publisher=params.publisher
        book.pubdate=params.pubdate
        book.price=Decimal(params.price)
        book.quantity=params.quantity
        book.series = params.series

        bookservice.updatebook(book)

        return render.bookedit(book,EditBook.aurl)


#TODO not implemented at the moment,because most of the book will be get from douban
class CreateBook():
    def GET(self):
        book=Book()
        return render.bookedit(book,URL_CREATE)

    def POST(self):
        #if uid is not null then add it to user at the same time
        params = web.input()
        uid =1
        book=Book()
        book.title=params.title
        book.subtitle=params.subtitle
        book.isbn10=params.isbn10
        book.isbn13=params.isbn13
        book.author=params.author
        book.translators.append(params.translators)
        book.publisher=params.publisher
        book.pubdate=params.pubdate
        book.price=Decimal(params.price)
        book.quantity=int(params.quantity)
        book.pages = int(params.pages)
        book.series = params.series

        bookservice.create_book(book)

        return render.common("OK")

class AddBook():
    def POST(self):
        params = web.input()
        #uid=params.uid
        uid=1
        bid=params.bid
        bookservice.add_userbook(uid,bid)

        return render.common("OK")

class DeleteBook():
    def GET(self,bid):
        bookservice.remove_book(int(bid))

        return render.common("OK")

if __name__=="__main__":
    app.run()



