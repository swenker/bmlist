from __future__ import unicode_literals

from django.db import models

from bmutils import *

# Create your models here.


"User registeration can be done by input username and passwd,email is used when password is forgotten"
class Account(models.Model):
    # id=0
    email=models.CharField(max_length=60,null=True,blank=True)
    passwd=models.CharField(max_length=20)
    nickname=models.CharField(max_length=20,null=True,blank=True)
    # cellphone=models.CharField(max_length=20,null=True,blank=True)
    dtcreate=models.DateTimeField(auto_now_add=True)
    status=models.SmallIntegerField(default=1)

    def __str__(self):
        return "id:%d,email:%s,status:%d" %(self.id,self.email,self.status)

    def jsonable2(self):
        return self.__dict__

    def jsonable(self):
        return dict(id=self.id,
                    email=self.email,passwd=self.passwd,nickname=self.nickname,
                    # cellphone=self.cellphone,
                    dtcreate = self.dtcreate,
                    status=self.status)



#TODO
class UserProfile(models.Model):
    # id=0
    brief = models.CharField(max_length=100, null=True, blank=True)
    #TODO foreign key?
    account_id = models.IntegerField(null=False)

    def __str__(self):
        return self.__unicode__().encode('utf8')

    def __unicode__(self):
        return "id:%s,brief:%s" \
        % (self.id,self.brief)

    def jsonable(self):
        return dict(
            id=self.id,brief=normalize_str(self.brief)
        )

