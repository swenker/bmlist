__author__ = 'samsung'
#coding=utf-8


from xml import sax
from entities import Book

class SavedBookHandler(sax.ContentHandler):
    """
         <book><isbn>9787200075366</isbn><title>1.9亿学生必读书 宋词</title><author>朱孝臧</author><publisher>第1版 (2009年1月1日)</publisher>
           <pubdate>2009-1</pubdate><pages>183</pages><price>19.9</price></book>
    """

    def __init__(self,datalist):
        self.buffer = []
        self.datalist = datalist
        self.book = None

    def startElement(self,name, attrs):
        self.buffer = []
        #print "start:"+name
        if "book" == name :
            self.book = Book()


    def endElement(self,name):

        if "isbn" ==name :
            self.book.isbn13 = "".join(self.buffer)

        #elif ("title" ==name):
        #    self.book.title = "".join(self.buffer)
        #
        #elif ("author" ==name):
        #    self.book.author = "".join(self.buffer)
        #
        #elif ("publisher" ==name):
        #    self.book.publisher = "".join(self.buffer)
        #
        #elif ("pubdate" == name):
        #    self.book.pubdate = "".join(self.buffer)
        #
        #elif ("pages" == name):
        #    self.book.pages = int(self.buffer)
        #
        #elif ("price" == name):
        #    self.book.price =  float(self.buffer)

        elif "book" == name :
            self.datalist.append(self.book.isbn13)

    def characters(self,content):
        self.buffer.append(content.strip())


class SavedBookParser():
    def __init__(self):
         self.savedbookparser=sax.make_parser()
         self.isbnlist=[]
         self.savedbookparser.setContentHandler(SavedBookHandler(self.isbnlist))

    def parse_saved_book(self,xmlResource):
         self.savedbookparser.parse(xmlResource)

def testparse():
    datafile=r"D:\work\projects\111-tech-bmlist\booklist.xml"
    parser=SavedBookParser()
    parser.parse_saved_book(datafile)
    isbnlist=parser.isbnlist
    print len(isbnlist)
    print isbnlist


if __name__=="__main__":
    testparse()