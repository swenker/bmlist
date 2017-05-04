from decimal import Decimal
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseServerError
from django.http import JsonResponse
from django.http import Http404

from  bmlist_service import book_service
from books.models import Book
from books.models import User


# Create your views here.
CONTENT_TYPE="application/json;charset=UTF-8"
def index(request):
    context ={ 'abc':'1234567890'}
    return render(request,'books/index.html',context)

def search_book(request):
    keyword = request.GET.get('k',None)
    npage = request.GET.get('np',1)
    total_count,total_pages,book_list = book_service.search_books(keyword,npage)
    # return HttpResponse(book.jsonable(),content_type="application/json")

    return JsonResponse( BookListWrapper(book_list, total_count, total_pages, npage).jsonable(),content_type=CONTENT_TYPE)

def get_book_detail(request,book_id):
    "The parameter is still in string format instead of int"
    book = book_service.get_book_by_id(book_id)
    if not book:
        raise Http404("Book with id %s Not Found" % book_id)

    return JsonResponse(book.jsonable())

def delete_book(request,book_id):
    if not book_service.delete_book(book_id):
        raise Http404("Book with id %s Not Found" % book_id)

    return HttpResponse("{'status':'OK'}")

def get_book_by_isbn(request,isbn):
    "search it locally,if not found then try to get it from remote service"
    book  = book_service.get_book_by_isbn(isbn)
    if book:
        json_response = JsonResponse(book.jsonable(),content_type=CONTENT_TYPE)
        # json_response._headers['X-Frame-Options']='*'
        return json_response
    else:
        raise Http404("Book with isbn %s Not Found" % isbn)

def get_GET_param(request, param_name, default_value=None):
    val = request.POST.get(param_name,default_value)
    print("%s:%s" %(param_name,val))
    return request.GET.get(param_name,default_value)

def get_POST_param(request, param_name, default_value=None):
    val = request.POST.get(param_name,default_value)
    print ("%s:%s" %(param_name,val))
    if val:
        val = val.strip()
    return val


def create_book(request):
        book=Book()


def add_book_to_user_shelf(request,book_id):
    pass


def __fill_in_user(request,user):
    user.email = get_POST_param(request, 'email')
    user.passwd = get_POST_param(request, 'passwd')
    user.nickname = get_POST_param(request, 'nickname')

def signup_user(request):
    user = User()
    __fill_in_user(request,user)



class UserListWrapper:
    "For json serialization"
    def __init__(self,ulist,total_count=0,total_pages=0,npage=0):
        "The item in blist should have a method named jsonable"
        self.itemlist =[ sitem.jsonable() for sitem in ulist ]
        self.total = total_count
        self.total_pages = total_pages
        self.npage = npage

    def jsonable(self):
        return self.__dict__
