__author__ = 'samsung'

import web
from entities import User
from bmservice import UserService,BookService
from bookparser import BookParser

urls=(
    '/bm','Home',
    '/bm/s','PrintService',
    '/bm/user/signin','UserSignin',
    '/bm/book/check','CheckBook',
    '/bm/book/list/(\d*)','ListBooks',
    '/bm/book/get/(\d+)', 'GetBook',
    '/bm/book/create','CreateBook',
    '/bm/book/delete?bid= [need to check privileges,only admin can do this]','DeleteBook',
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
        end=1000
        if(not uid):
            booklist = bookservice.list_books(start,end)

        elif uid>0:
            booklist = bookservice.list_user_books(int(uid),start,end)

        return render.booklist(booklist)

class CheckBook():
    def GET(self,isbn=None):
        params = web.input()
        isbn = params.isbn

        bookparser = BookParser()
        book = bookparser.parsebookbyisbn(isbn)

        return render.book(book,isbn)


class GetBook():
    def GET(self,bid):
        book = bookservice.get_book_byid(bid)

        return render.book(book,book.isbn13)


#TODO not implemented at the moment,because most of the book will be get from douban
class CreateBook():
    def POST(self):
        #if uid is not null then add it to user at the same time
        params = web.input()
        uid =1
        isbn = params.isbn

        bookservice.insert_book(isbn,uid)

        return "OK"

class AddBook():
    def POST(self):
        params = web.input()
        #uid=params.uid
        uid=1
        bid=params.bid
        bookservice.add_userbook(uid,bid)

        return "OK"

class DeleteBook():
    def POST(self):
        params = web.input()
        bid = params.bid



if __name__=="__main__":
    app.run()



