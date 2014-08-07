__author__ = 'samsung'

from decimal import *
import json
import web

from entities import *
from bmservice import AccountService
from bmservice import BookService



URL_CREATE='/bm/book/create'
URL_EDIT='/bm/book/edit'
URL_GET='/bm/book/get'
URL_CHECK='/bm/book/check'
URL_LIST='/bm/book/list'
URL_DELETE='/bm/book/delete'
URL_IMPORT='/bm/book/imp'
URL_EXPORT='/bm/book/exp'
URL_SIGNIN='/bm/u/signin'
URL_SIGNOUT='/bm/u/sout'

urls=(
    '/bm','Home',
    '/bm/s','DisplayService',
    URL_CHECK,'CheckBook',  #mainly used to record book into database
    URL_LIST,'ListBooks',
    URL_GET, 'GetBook',
    URL_EDIT, 'EditBook',
    URL_CREATE,'CreateBook',
    URL_DELETE,'DeleteBook',
    URL_IMPORT,'ImportBook',
    URL_EXPORT,'ExportBook',
    '/bm/book/add','AddBook',
    URL_SIGNIN,'UserSignin',
    URL_SIGNOUT,'UserSignout'
)
web.config.debug = False
app=web.application(urls,globals())
application = app.wsgifunc()

session = web.session.Session(app, web.session.DiskStore('sessions.bm'), initializer={'bmuser': None})
render = web.template.render("templates")

bookservice = BookService()

class Home():
    def GET(self):
        return render.index()

class DisplayService():
    def GET(self):
        return urls


def updatesession(user):
    session.bmuser=user

def checksession():
    return session.bmuser

class UserSignin():
    def GET(self):
        if not checksession():
            return render.signin()
        else:
            return render.index()

    def POST(self):
        params = web.input()
        email = params.email
        passwd= params.passwd

        account_service=AccountService()
        bmuser=account_service.signin(email,passwd)
        if bmuser:
            updatesession(bmuser)
            return render.index()
        else:
            updatesession(None)
            return render.error("Failded to login in")

class UserSignout():
    def GET(self):
        if checksession():
            session.kill()

        return render.index()


_EVERY_PAGE=20
class ListBooks():
    def GET(self):
        params = web.input(uid=None,np=0,kw=None)

        uid=params.uid

        npages=int(params.np)
        start=(npages)*_EVERY_PAGE
        nfetch =_EVERY_PAGE

        keyword=params.kw
        if keyword:
            keyword = keyword.strip()

        blist=None
        total=0

        if not uid :
            blist,total = bookservice.list_books(start,nfetch,keyword)

        else:
            blist = bookservice.list_user_books(uid,start,nfetch)

        total_pages=(total+_EVERY_PAGE-1)/_EVERY_PAGE

        logged=False
        if checksession():
            logged=True

        return render.booklist(blist,total,total_pages,logged)

class CheckBook():
    def GET(self):
        params = web.input()
        isbn = params.isbn.strip()
        book=bookservice.get_book_byisbn(isbn)
        if book :
            return render.bookview(book)
        else:
            book = bookservice.get_book_byisbn_fromremote(isbn)
            if not book :
                book=Book()
            return render.bookedit(book,URL_CREATE)


class GetBook():
    def GET(self):
        params = web.input()
        bid = params.bid

        book = bookservice.get_book_byid(bid)

        return json.dumps(book,cls=ComplexEncoder)


class EditBook():
    def POST(self):
        """To save book """
        params=web.input()
        ServiceHelper().savebook(params)

        return render.common("OK")



class CreateBook():
    def GET(self):
        book=Book()
        return render.bookedit(book,URL_CREATE)

    def POST(self):
        #if uid is not null then add it to user at the same time
        params = web.input()
        ServiceHelper().savebook(params)

        return render.common("OK")


class AddUserBook():
    def POST(self):
        params = web.input()
        #uid=params.uid
        uid=1
        bid=params.bid
        bookservice.add_userbook(uid,bid)

        return render.common("OK")

class DeleteBook():
    def GET(self):
        params = web.input()
        bid = params.bid

        bookservice.remove_book(int(bid))

        return render.common("OK")

class ImportBook():
    """export book and import book"""
    def GET(self):
        isbnparsed,isbnfailed=bookservice.import_book()

        result="total:%d,failed isbn:%s" %(isbnparsed,isbnfailed)
        return  render.common(result)

    #upload file and import it
    def POST(self):
        pass

class BookBackup():
    """export book"""
    def GET(self):
        pass

    #upload file and import it
    def POST(self):
        pass


class ServiceHelper():

    def savebook(self,params):
        bid=int(params.bid)
        book=None
        if bid:
            book = bookservice.get_book_byid(bid)
        else:
            book=Book()

        book.title=params.title
        book.subtitle=params.subtitle
        book.isbn10=params.isbn10
        book.isbn13=params.isbn13
        book.author=params.author
        if params.translators :
            book.translators = params.translators.split(";")
        book.publisher=params.publisher
        book.pubdate=params.pubdate
        book.price=Decimal(params.price)
        book.quantity=int(params.quantity)
        book.pages = int(params.pages)
        book.series = params.series

        if bid :
            bookservice.updatebook(book)
        else:
            bookservice.create_book(book)

        return book

#It can not be run on Windows
if __name__=="__main__":
    app.run()



