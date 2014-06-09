__author__ = 'samsung'

class MyException(BaseException):
    pass

def test_expected():
    raise MyException("Exist")

def test_string():
    abc=['你好','中文']
    print abc

test_expected()
