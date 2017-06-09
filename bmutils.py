__author__ = 'wenjusun'

from datetime import datetime
def normalize_str(str):
    if str:
        return str.strip()
    else:
        return ""


def get_now():
    return datetime.now()

def get_GET_param(request, param_name, default_value=None):
    val = request.GET.get(param_name,default_value)
    # print("%s:%s" %(param_name,val))
    if val:
        val = val.strip()
    else:
        val = default_value
    return val

def get_POST_param(request, param_name, default_value=None):
    val = request.POST.get(param_name, default_value)
    # print ("%s:%s" % (param_name, val))
    if val:
        val = val.strip()
    else:
        val = default_value
    return val


class PaginationListWrapper:
    "For json serialization"
    def __init__(self,ulist,total_count=0,total_pages=0,npage=0):
        "The item in blist should have a method named jsonable"
        self.itemlist =[ sitem.jsonable() for sitem in ulist ]
        self.total = total_count
        self.total_pages = total_pages
        self.npage = npage

    def jsonable(self):
        return self.__dict__
