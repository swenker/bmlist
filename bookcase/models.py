from __future__ import unicode_literals

from django.db import models

# Create your models here.
from books.models import Book

class Bookcase(models.Model):
    uid = models.IntegerField(null=False)
    create_time = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(default=1)
    title = models.CharField(max_length=20, null=True, blank=True)
    books = models.ManyToManyField(to=Book)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.__unicode__().encode('utf8')

    def jsonable(self):
        return self.__dict__


"""
class Bookcase(models.Model):
    uid = models.IntegerField(null=False)
    create_time = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(default=1)
    title = models.CharField(max_length=20, null=True, blank=True)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.__unicode__().encode('utf8')

    def jsonable(self):
        return self.__dict__


class Booklist(models.Model):
    bookcase_id = models.IntegerField(null=False)
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.__unicode__().encode('utf8')

    def jsonable(self):
        return self.__dict__

"""


