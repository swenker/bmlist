__author__ = 'samsung'

from bmservice import BookService
import logging

def testimport():
    BookService().importbook()

def testexport():
    BookService().exportbook()

def testgetbook(bid):
    book=BookService().get_book_byid(bid)
    print book

def testupdate(bid):
    bs=BookService()
    book=bs.get_book_byid(bid)
    bs.updatebook(book)

    print book

if __name__=="__main__":
    #testimport()
    testupdate(432)
    testgetbook(432)
    #testexport()
    #logger=logging.Logger("abc")
    #logger.debug("")

