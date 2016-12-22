__author__ = 'wenjusun'
import json
from decimal import *
from datetime import datetime

from bmutils import *

class Book(object):
    id=0
    title=''
    subtitle=''
    isbn10=''
    isbn13=''
    author=''
    translators=[]
    transtr=''
    publisher=''
    pubdate=''
    price=Decimal(0)
    pages=0
    update_time=None
    create_time=None
    quantity=1
    binding=''
    series=''
    keywords=''
    summary=''
    authorintro=''
    status=1

    def _transtr(self):
        if self.translators:
            tmpstr=""
            for st in self.translators:
                tmpstr=tmpstr+st.strip()+";"
            self.transtr=tmpstr[:-1]

            print self.transtr
            return self.transtr

    def __str__(self):
        return self.__unicode__().encode('utf8')

    def __unicode__(self):
        return "id:%s,isbn10:%s,isbn13:%s,title:%s,subtitle:%s,author:%s,translators:%s,binding:%s,"\
        "publisher:%s,pubdate:%s,price:%s,pages:%d,update_time:%s,create_time:%s,quantity:%d,series:%s,keywords:%s,summary:%s,authorintro:%s" \
        % (self.id,self.isbn10,self.isbn13,self.title,self.subtitle,self.author,";".join(self.translators), self.binding,
           self.publisher,self.pubdate,self.price,self.pages,self.update_time,self.create_time,self.quantity,self.series,"","","")
           #self.publisher,self.pubdate,self.price,self.pages,self.update_time,self.create_time,self.quantity,self.series,self.keywords,self.summary,self.authorintro)

    def jsonable(self):
        #return self.__dict__
        return dict(
            id=self.id, isbn10=self.isbn10, isbn13=self.isbn13, title=self.title, subtitle=self.subtitle, author=self.author,
            transtr=normalize_str(self._transtr()), binding=self.binding, publisher=self.publisher, pubdate=self.pubdate, price=self.price,
            pages=self.pages, update_time=self.update_time, create_time=self.create_time, quantity=self.quantity, series=normalize_str(self.series),
            keywords=normalize_str(self.keywords), summary=normalize_str(self.summary),authorintro=normalize_str(self.authorintro)
        )


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'jsonable'):
            return obj.jsonable()
        elif isinstance(obj,datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(obj,Decimal):
            return str(obj)
        else:
            raise TypeError, 'Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj))

