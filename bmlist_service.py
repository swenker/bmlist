__author__ = 'wenjusun'

import re
import hashlib

from django.db.models.query_utils import Q
from django.core.paginator import Paginator

from serviceconfig import logger
from books.models import Book
from users.models import Account
# from bookcase.models import Bookcase
from bookparser import BookParser
from bmutils import *

isbn10_pattern=re.compile('\d{10}')
isbn13_pattern=re.compile('\d{13}')





class UserAccountService():
    def __is_email(self,input_email):
        if input_email and input_email.count('@') == 1:
            return True
        return False

    def signin(self,passwd,login_id):
        passwd = tomd5(passwd)
        if self.__is_email(login_id):
            email = login_id.lower()
            try:
                account = Account.objects.get(email=email.lower())
                if account:
                    #TODO compare char by char?
                    if account.passwd == passwd:
                        return account
            except Account.DoesNotExist as dne:
                return None

        else:
            nickname = login_id
            account = Account.objects.get(nickname = nickname)
            try:
                if account:
                    if account.passwd == passwd:
                        return account
            except Account.DoesNotExist as dne:
                return None

        return None

    def signup(self,account):
        """new account"""
        passwd=tomd5(account.passwd)
        if not self.__exists(account.email,account.nickname):
            account.passwd = passwd
            account.save()
            return account.id
        else:
            msg="email:%s already exist."%(account.email)
            logger.info(msg)
            raise BaseException(msg)

    def __exists(self,email,nickname):
        email = email.lower()
        try:
            account = Account.objects.get(email = email)
            if account:
                return Account
            else:
                account = Account.objects.get(nickname = nickname)
            if account:
                return True

        except Account.DoesNotExist as dne:
            return False

    def delete_account(self,account_id):
        account = Account.objects.get(id=account_id)
        account.delete()

    def search_accounts(self, keyword, npage=1):
        "If no keyword is passed in , the result is top new accounts recently signup."
        account_list=None
        total_count=0
        total_pages=0
        N_EVERY_PAGE=2

        if keyword:
            if self.__is_email(keyword):
                account_list = Account.objects.filter(email = keyword)
            else :
                account_list = Account.objects.filter(nickname = keyword)
        else:
            account_list = Account.objects.all().order_by('-dtcreate')

        if account_list:
            total_count = len(account_list)
            total_pages = (total_count+N_EVERY_PAGE-1)/N_EVERY_PAGE

            paginator = Paginator(account_list,N_EVERY_PAGE)
            account_list = paginator.page(npage)

        return total_count,total_pages,account_list

    def change_passwd(self,uid,oldpwd,newpwd):
        raise BaseException("Not Implemented")

"""
class BookcaseService():
    def get_bookcase_list(self,user_id):
        bookcase_list = Bookcase.objects.filter(uid = user_id).order_by('-create_time')
        return bookcase_list

    def search_books(self,user_id,keywords,npage):
        raise Book.DoesNotExist()

    def add_to_bookcase(self,user_id,book_id):
        bookcase_list = self.get_bookcase_list(user_id)
        if bookcase_list:
            bookcase = bookcase_list[0]
"""


book_service = BookService()
user_service = UserAccountService()
