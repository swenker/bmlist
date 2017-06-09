from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.db.models import Model


class XNote(Model):
    title=models.CharField(max_length=60, null=True, blank=True)
    # content=models.CharField(max_length=2000, null=True, blank=True)
    content=models.TextField(null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True, blank=False)
    update_time= models.DateTimeField(auto_now_add=True, blank=False)
    uid = models.IntegerField(null=False,default=0)
    status = models.SmallIntegerField(null=False,default=1)

    def __str__(self):
        return self.__unicode__().encode('utf8')

    def __unicode__(self):
        return "id:%d, title:%s,content:%s,create_time:%s,update_time:%s,uid:%d,status:%s,"\
               %(self.id,self.title,self.content,self.create_time,self.update_time,self.uid,self.status)


    def jsonable(self):
        return dict(id=self.id,title = self.title,content = self.content,
                    create_time = self.create_time,update_time = self.update_time,uid = self.uid,status = self.status)