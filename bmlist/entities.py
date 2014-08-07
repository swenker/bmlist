#! /usr/bin/env python
#coding=utf-8
import json
from decimal import *

class User(object):
    def __init__(self):
        self.id=0
        self.email=''
        self.passwd=''
        self.nickname=''
        self.cellphone=''
        self.status=1

    def __str__(self):
        return "id:%d,email:%s,status:%d" %(self.id,self.email,self.status)

    def jsonable(self):
        return self.__dict__

class Book(object):
    def __init__(self):
        self.id=0
        self.title=''
        self.subtitle=''
        self.isbn10=''
        self.isbn13=''
        self.author=''
        self.translators=[]
        self.transtr=''
        self.publisher=''
        self.pubdate=''
        self.price=Decimal(0)
        self.pages=0
        self.update_time=None
        self.create_time=None
        self.quantity=1
        self.binding=1
        self.series=''
        self.keywords=''    
        self.summary=''
        self.authorintro=''
        self.status=1

    def _transtr(self):
        if self.translators:
            tmpstr=""
            for st in self.translators:
                tmpstr=tmpstr+st.strip()+";"

            self.transtr=tmpstr[:-1]

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
        return self.__dict__

class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'jsonable'):
            return obj.jsonable()
        else:
            raise TypeError, 'Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj))

