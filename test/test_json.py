__author__ = 'sunwj'

import json
from datetime import datetime
from decimal import Decimal

class Address:
    def __init__(self,street):
        self.street=street
        self.houses=[]

    def jsonable(self):
        return self.__dict__


class Person(object):
    def __init__(self,name,address):
        self.name=name
        self.address=address

    def toJSON(self):
        return self.__dict__


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'jsonable'):
            return obj.jsonable()
        else:
            raise TypeError, 'Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj))

class ComplexListEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'jsonable'):
            return obj.jsonable()
        elif isinstance(obj,list):
            pass
        else:
            raise TypeError, 'Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj))

class DatetimeTest():
    def __init__(self,name):
        self.dtime=datetime.now()
        self.strname=name
        self.address=Address("abc")
        self.price=Decimal("12")

    def jsonable(self):
        return self.__dict__


class MyDatetimeEncoder(json.JSONEncoder):
    def default(self, obj):
        print type(obj)
        if hasattr(obj, 'jsonable'):
            return obj.jsonable()
        elif isinstance(obj,datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(obj,Decimal):
            return str(obj)
        # else:
        #     raise TypeError, 'Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj))
        else:
            return obj.__dict__


pn=Person("Mike",Address("Taiyanggong"))

pn2=Person("Tom",Address("Hepingjie"))

plist=[pn,pn2]


#{"name": "Mike", "address": {"street": "Taiyanggong"}}
# print json.dumps(pn.__dict__,cls=ComplexEncoder)
# print json.dumps(list,cls=ComplexEncoder)
#json.dumps([unicode(t) for t in tags_found]) or json.dumps(map(unicode, tags_found))
#print json.dumps([p.__dict__ for p in plist],cls=ComplexEncoder)

print json.dumps(DatetimeTest("Hello").__dict__,cls=MyDatetimeEncoder)
