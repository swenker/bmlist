__author__ = 'samsung'

import unittest
import logging
import logging.config
from bmlist.bmservice import *

logging.config.fileConfig(r"conf/local/log.cfg")

logger=logging.getLogger("BmService")


class TestAccountService(unittest.TestCase):
    def test_checkuser(self):
        logger.warn("Hello,I am log")
        #logging.warn("Hello,I am log")
        self.assertEqual(1,1)

    def test_signin(self):
        self.assertTrue(AccountService().signin('swenker@126.com','koob'))
        self.assertIsNone(AccountService().signin('swenker@126.com','koob1'))

    def test_signup(self):
        pass



class TestBookService(unittest.TestCase):
    def setUp(self):
        self.bookService=BookService()

    @unittest.skip("skipping")
    def test_list_user_books(self):
        uid=1
        books=self.bookService.list_user_books(uid,0,10)
        self.assertTrue(books)
        #print books

    def test_list_books(self):
        books=self.bookService.list_books(0,10)
        self.assertTrue(books)
        print books

    def test_get_book_by_bid(self):
        bid=432
        book=self.bookService.get_book_byid(bid)
        self.assertTrue(book)

        #print book

    def test_get_book_by_isbn(self):
        isbn="9787111095439"
        book=self.bookService.get_book_byisbn(isbn)
        self.assertTrue(book)

        #print book

    @unittest.skip("passed")
    def test_insert_book(self):
        isbn="9787111095439"
        self.bookService.insert_book(isbn)


    @unittest.skip("skipping")
    def test_update_book(self):
        bid=1
        bs=BookService()
        book=bs.get_book_byid(bid)
        bs.updatebook(book)

        #print book

    @unittest.skip("skipping")
    def test_import_books(self):
        BookService().import_book()

    @unittest.skip("skipping")
    def test_export_books(self):
        BookService().export_book()


def run_test():
    suite1 = unittest.TestLoader().loadTestsFromTestCase(TestBookService)
    suite2 = unittest.TestLoader().loadTestsFromTestCase(TestAccountService)
    alltests = unittest.TestSuite([suite1, suite2])
    unittest.TextTestRunner(verbosity=2).run(alltests)


if __name__=="__main__":
    unittest.main()
