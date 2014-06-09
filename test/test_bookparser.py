__author__ = 'samsung'

import unittest
from bmlist import bookparser
from bmlist.serviceconfig import *

class TestBookParser(unittest.TestCase):
    def setUp(self):
        self.bookParser=bookparser.BookParser()
        self.logger = bmconfig.getlogger()

    @unittest.skip("Skipping")
    def test_parse_book_from_xml(self):
        self.bookParser.parsebook("")

    def test_parse_book_byisbn(self):
        book = self.bookParser.parsebookbyisbn('9787543639133')
        self.logger.debug(book)

    def test_parse_book_byisbn_none(self):
        book = self.bookParser.parsebookbyisbn('9777543639133')

        self.assertIsNone(book)

def run_test():
    suit1 = unittest.TestLoader().loadTestsFromTestCase(TestBookParser)
    unittest.TextTestRunner(verbosity=3).run(suit1)

if __name__ == "__main__":
    unittest.main()
