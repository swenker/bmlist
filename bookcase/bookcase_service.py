from django.core.paginator import Paginator

from bookcase.models import Bookcase
from books.models import Book

N_EVERY_PAGE = 2


class BookcaseService():
    def get_default_bookcase(self, user_id, bookcase_id=None):
        if not bookcase_id:
            bookcase_list=None
            try:
                bookcase_list = Bookcase.objects.get(uid=user_id)
            except:
                pass

            if bookcase_list:
                if isinstance(bookcase_list,list):
                    bookcase = bookcase_list[0]
                else:
                    bookcase = bookcase_list
            else:
                bookcase = Bookcase()
                bookcase.title = 'Default Bookcase'
                bookcase.uid = user_id
                bookcase.save()
        else:
            bookcase = Bookcase.objects.get(id=bookcase_id)

        return bookcase

    def get_bookcase_list(self, user_id):
        bookcase_list = Bookcase.objects.filter(uid=user_id).order_by('title')
        return bookcase_list

    def search_books(self, user_id, keywords, npage):

        bookcase = self.get_default_bookcase(user_id)
        try:
            if keywords:
                book_list = bookcase.books.get(title=keywords)
            else:
                book_list = bookcase.books.all()

            total_count = len(book_list)
            total_pages = (total_count + N_EVERY_PAGE - 1) / N_EVERY_PAGE

            paginator = Paginator(book_list, N_EVERY_PAGE)
            book_list = paginator.page(npage)

            return total_count, total_pages, book_list
        except Book.DoesNotExist,dne:
            print dne
            return None

    def add_book(self, user_id, book_id, bookcase_id=None):

        book = Book.objects.get(id=book_id)
        bookcase = self.get_default_bookcase(user_id, bookcase_id)
        bookcase.books.add(book)
        bookcase.save()

        return True

    def remove_books(self, user_id, book_id, bookcase_id):
        bookcase = self.get_default_bookcase(user_id, bookcase_id)
        book = Book.objects.get(id=book_id)
        bookcase.books.remove(book)

    def get_book(self, user_id, book_id, bookcase_id):
        bookcase = self.get_default_bookcase(user_id, bookcase_id)
        try:
            book = bookcase.books.get(id=book_id)
            return book.id
        except Book.DoesNotExist, dne:
            return None

bookcase_service = BookcaseService()
