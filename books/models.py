from __future__ import unicode_literals
from decimal import Decimal
from datetime import datetime

from django.db import models

from bmutils import *

# Create your models here.
class Book(models.Model):
    # id=0
    title = models.CharField(max_length=60)
    subtitle = models.CharField(max_length=60, null=True, blank=True)
    isbn10 = models.CharField(max_length=10, null=True, blank=True)
    isbn13 = models.CharField(max_length=13, null=True, blank=True)
    author = models.CharField(max_length=80)
    # translators = []
    transtr = models.CharField(max_length=100, null=True, blank=True)

    publisher = models.CharField(max_length=60)
    pubdate = models.CharField(max_length=10)
    price = models.DecimalField(default=0, max_digits=5, decimal_places=2)  # max 999.99
    pages = models.IntegerField(default=0)
    update_time = models.DateTimeField(auto_now_add=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True, blank=True)
    quantity = models.SmallIntegerField(default=1)
    binding = models.CharField(max_length=10, null=True, blank=True)
    series = models.CharField(max_length=40, null=True, blank=True)
    keywords = models.CharField(max_length=40, null=True, blank=True)
    summary = models.CharField(max_length=500, null=True, blank=True)
    authorintro = models.CharField(max_length=500, null=True, blank=True)
    status = models.SmallIntegerField(default=1)

    # def __init__(self): #this will leads to instance initialization error
    #     self.create_time = datetime.now()
    #     self.update_time = self.create_time

    # def _transtr(self):
    #     if self.translators:
    #         tmpstr=""
    #         for st in self.translators:
    #             tmpstr=tmpstr+st.strip()+";"
    #         self.transtr=tmpstr[:-1]
    #         return self.transtr

    def __str__(self):
        return self.__unicode__().encode('utf8')

    def __unicode__(self):
        return "id:%s,isbn10:%s,isbn13:%s,title:%s,subtitle:%s,author:%s,transtr:%s,binding:%s,"\
        "publisher:%s,pubdate:%s,price:%s,pages:%d,update_time:%s,create_time:%s,quantity:%d,series:%s,keywords:%s,summary:%s,authorintro:%s" \
        % (self.id,self.isbn10,self.isbn13,self.title,self.subtitle,self.author,self.transtr, self.binding,
           self.publisher,self.pubdate,self.price,self.pages,self.update_time,self.create_time,self.quantity,self.series,"","","")
           #self.publisher,self.pubdate,self.price,self.pages,self.update_time,self.create_time,self.quantity,self.series,self.keywords,self.summary,self.authorintro)


    # def jsonable(self):
    #     "There are some properties in the parent class that can be not serializable simply"
    #     return self.__dict__

    def jsonable(self):
        return dict(
            id=self.id, isbn10=self.isbn10, isbn13=self.isbn13, title=self.title, subtitle=self.subtitle, author=self.author,
            transtr=normalize_str(self.transtr), binding=self.binding, publisher=self.publisher, pubdate=self.pubdate, price=self.price,
            pages=self.pages, update_time=self.update_time, create_time=self.create_time, quantity=self.quantity, series=normalize_str(self.series),
            keywords=normalize_str(self.keywords), summary=normalize_str(self.summary),authorintro=normalize_str(self.authorintro)
        )

class Comment:
    title = models.CharField(max_length=60, null=True, blank=True)
    content = models.CharField(max_length=2000, null=True, blank=True)

    def __init__(self,title,content,ctime,uid):
        self.title = title
        self.content = content
        self.ctime = None
        self.uid = uid

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.__unicode__().encode('utf8')

    def jsonable(self):
        return self.__dict__
