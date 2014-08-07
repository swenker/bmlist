__author__ = 'sunwj'

import json

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


pn=Person("Mike",Address("Taiyanggong"))

pn2=Person("Tom",Address("Hepingjie"))

plist=[pn,pn2]


#{"name": "Mike", "address": {"street": "Taiyanggong"}}
# print json.dumps(pn.__dict__,cls=ComplexEncoder)
# print json.dumps(list,cls=ComplexEncoder)
#json.dumps([unicode(t) for t in tags_found]) or json.dumps(map(unicode, tags_found))
print json.dumps([p.__dict__ for p in plist],cls=ComplexEncoder)
