from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Comment(models.Model):
    title = models.CharField(max_length=60, null=True, blank=True)
    content = models.CharField(max_length=2000, null=True, blank=True)
    dtcreate = models.DateTimeField(auto_now_add=True)
    bkid=models.IntegerField()
    uid=models.IntegerField()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.__unicode__().encode('utf8')

    def jsonable(self):
        return self.__dict__
