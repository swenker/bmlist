__author__ = 'wenjusun'

import re
import hashlib

from django.db.models.query_utils import Q
from django.core.paginator import Paginator

from serviceconfig import logger
from books.models import Book
from books.models import User
from bookparser import BookParser
from bmutils import *

isbn10_pattern=re.compile('\d{10}')
isbn13_pattern=re.compile('\d{13}')

def tomd5(s):
    md5handler=hashlib.md5(s)
    return md5handler.hexdigest()

class BookService():
    bookParser = BookParser()

    def create_book(self,book):
        book.save()
        return book.id

    def search_books(self, keyword, npage=1):
        "If no keyword is passed in , the result is top new books recently added."
        book_list=None
        total_count=0
        total_pages=0
        N_EVERY_PAGE=2

        if keyword:
            if isbn13_pattern.match(keyword):
                book_list = Book.objects.filter(isbn13 = keyword)
            elif isbn10_pattern.match(keyword):
                book_list = Book.objects.filter(isbn10 = keyword)
            else:
                book_list = Book.objects.filter(Q(title__icontains = keyword)
                                                | Q(publisher__icontains = keyword)
                                                | Q(author__icontains = keyword)
                                               )
        else:
            book_list = Book.objects.all().order_by('-create_time')
        if book_list:
            total_count = len(book_list)
            total_pages = (total_count+N_EVERY_PAGE-1)/N_EVERY_PAGE

            paginator = Paginator(book_list,N_EVERY_PAGE)
            book_list = paginator.page(npage)

        return total_count,total_pages,book_list

    def get_book_by_isbn(self,isbn):
        "Query locally"
        book=None
        try:
            if isbn13_pattern.match(isbn):
                book = Book.objects.filter(isbn13=isbn)
            elif isbn10_pattern.match(isbn):
                book = Book.objects.filter(isbn10=isbn)
            if book:
                return book[0]
        except Book.DoesNotExist, dne:
            from django.db import connection
            print connection.queries
            # print dne
        return None

    def get_book_byisbn_fromremote(self,isbn):
        return self.bookParser.parsebookbyisbn(isbn)

    def get_book_by_id(self,book_id):
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist,dne:
            return None
        return book

    def delete_book(self,book_id):
        try:
            book = Book.objects.get(id=book_id)
            book.delete()
        except Book.DoesNotExist,dne:
            return None
        return True

    def update_book(self,book):
        try:
            old_book = Book.objects.get(id=book.id)
            old_book.title = book.title
            old_book.subtitle = book.subtitle
            old_book.isbn10 = book.isbn10
            old_book.isbn13 = book.isbn13
            old_book.author = book.author
            old_book.transtr = book.transtr
            old_book.publisher = book.publisher
            old_book.pubdate = book.pubdate
            old_book.price = book.price
            old_book.pages = book.pages
            old_book.update_time = get_now()
            # old_book.create_time=book.create_time
            old_book.quantity = book.quantity
            old_book.binding = book.binding
            old_book.series = book.series
            old_book.keywords = book.keywords
            old_book.summary = book.summary
            old_book.authorintro = book.authorintro
            # old_book.status=book.status

            old_book.save()

        except Book.DoesNotExist,dne:
            return None
        return True



class UserAccountService():
    def signin(self,email,passwd):
        email = email.lower()
        passwd=tomd5(passwd)
        user = User.objects.get(email=email.lower())
        if user:
            #TODO compare char by char?
            if user.passwd == passwd:
                return user

        return None

    def signup(self,user):
        """new user"""
        passwd=tomd5(user.passwd)
        if not self.exists(user.email):
            user.passwd = passwd
            user.save()
        else:
            msg="email:%s already exist."%(user.email)
            logger.info(msg)
            raise BaseException(msg)

    def exists(self,email):
        email = email.lower()

        try:
            user = User.objects.get(email = email)
            if user:
                return True
        except User.DoesNotExist,dne:
            return False

    def delete(self,user_id):
        user = User.objects.get(id=user_id)
        user.delete()

    def changePasswd(self,uid,oldpwd,newpwd):
        raise BaseException("Not Implemented")


book_service = BookService()
