#! /usr/bin/env python
#coding=utf-8

"""Find book from remote service provider to get the detail information"""

import urllib
from xml import sax
from entities import Book
import re


SERVICE_URL = "http://api.douban.com/book/subject/isbn/"

def search_book(isbn):
    bookInfo = urllib.urlopen(SERVICE_URL+isbn)
    #    print bookInfo.geturl()
    return bookInfo.read()


class SimpleHandler(sax.ContentHandler):
    "simple sax handler to parse the xml from douban"
    def __init__(self,bookHolder):
        self.buffer = []
        self.book = bookHolder
        self.itemName = ""
        self.pPages = re.compile("([0-9]+)\\D*");
        self.pPrice = re.compile("([0-9]*\\.[0-9]{0,2})(\\D*)");


    def startElement(self,name, attrs):
        self.buffer = []
        #print "start:"+name
        if( "db:attribute" == name):
            self.itemName = attrs.getValue('name')
            
    def endElement(self,name):
        
        if( "db:attribute" == name): 
            #print "%d,%s" %(len(self.buffer),"".join(self.buffer))
            if ("isbn10" ==self.itemName):                
                self.book.isbn10 = "".join(self.buffer)
                
            elif ("isbn13" ==self.itemName):                
                self.book.isbn13 = "".join(self.buffer)
                
            elif ("title" ==self.itemName):                
                self.book.title = "".join(self.buffer)

            elif ("subtitle" ==self.itemName):                

                self.book.subtitle = "".join(self.buffer)
                
            elif ("author" ==self.itemName):                
                self.book.author = "".join(self.buffer)

            elif ("publisher" ==self.itemName):                
                self.book.publisher = "".join(self.buffer)

            elif ("pubdate" == self.itemName):                
                self.book.pubdate = "".join(self.buffer)

            elif ("format" ==self.itemName):                
                self.book.format = "".join(self.buffer)

            elif ("binding" == self.itemName):                
                self.book.binding = "".join(self.buffer)
                
            elif ("series" == self.itemName):                
                self.book.series = "".join(self.buffer)
                
            elif ("keywords" == self.itemName):                
                self.book.keywords = "".join(self.buffer)
                                
            elif ("author-intro" == self.itemName):                
                self.book.authorintro = "".join(self.buffer)

                
            #there maybe multiple translators    
            elif ("translator" == self.itemName):                
                self.book.translators.append("".join(self.buffer))
                
            elif ("quantity" == self.itemName):                
                self.book.quantity = "".join(self.buffer)

            elif ("pages" == self.itemName):       
         
                self.book.pages = 0
                matcher = self.pPages.match("".join(self.buffer))
                if (matcher):
                    self.book.pages = int(matcher.group(1))


            elif ("price" == self.itemName):       
         
                self.book.price = 0.0
                matcher = self.pPrice.match("".join(self.buffer))
                
                if matcher :
                    self.book.price = float(matcher.group(1))
        elif('summary' == name):
                self.book.summary = "".join(self.buffer)
        
    def characters(self,content):        
        self.buffer.append(content.strip())


class BookParser(object):
     def __init__(self):
         self.book = Book()
         self.parser=sax.make_parser()
         self.parser.setContentHandler(SimpleHandler(self.book))
       
     #url or filepath    
     def parsebook(self,xmlResource):
         self.parser.parse(xmlResource)

         return self.book
    
     def parsebookbyisbn(self,isbn):

         self.parser.parse(SERVICE_URL+isbn)

         return self.book

if __name__=='__main__':
    print "module debug.."       
    bookParser = BookParser() 
    xmlfile = r"D:\work\projects\bmlist\python\isbn.xml"
    #print bookParser.parseBook(xmlfile).__unicode__()
    #print bookParser.parseBook("http://api.douban.com/book/subject/isbn/"+'9787508353944').__unicode__()        
    print bookParser.parsebookbyisbn('9787508353944').__unicode__()
    
#print search_book('9787508353944')


 
    
     