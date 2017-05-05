__author__ = 'wenjusun'

from datetime import datetime
def normalize_str(str):
    if str:
        return str.strip()
    else:
        return ""


def get_now():
    return datetime.now()


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
