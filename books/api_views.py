from decimal import Decimal
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseServerError
from django.http import JsonResponse
from django.http import Http404

from books.book_service import book_service
from books.models import Book
from bmutils import PaginationListWrapper
from bmutils import get_POST_param,get_GET_param

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

    return JsonResponse( PaginationListWrapper(book_list, total_count, total_pages, npage).jsonable(),content_type=CONTENT_TYPE)

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

def get_book_by_isbn_for_add(request,isbn):
    "search it locally,if not found then try to get it from remote service"
    # isbn = get_GET_param(request,'isbn','')
    book  = book_service.get_book_by_isbn(isbn)
    if book:
        # return JsonResponse(book.jsonable(),content_type="application/json;charset=UTF-8",X_Frame_Options="*")
        json_response = JsonResponse(book.jsonable(),content_type=CONTENT_TYPE)
        # json_response._headers['X-Frame-Options']='*'
        return json_response
    else:
        book=book_service.get_book_byisbn_fromremote(isbn)
        book.id=''
        if book :
             return JsonResponse(book.jsonable(),content_type=CONTENT_TYPE)
        else:
            raise Http404("Book with isbn %s Not Found" % isbn)

def fill_in_book(request,book):
    book.title=get_POST_param(request,'title')
    book.subtitle=get_POST_param(request,'subtitle')
    book.isbn10=get_POST_param(request,'isbn10')
    book.isbn13=get_POST_param(request,'isbn13')
    book.author=get_POST_param(request,'author')
    transtr = get_POST_param(request,'transtr')
    if transtr:
        book.transtr = transtr

    book.publisher=get_POST_param(request,'publisher')
    book.pubdate=get_POST_param(request,'pubdate')
    book.price=Decimal(get_POST_param(request,'price',0))
    book.quantity=int(get_POST_param(request,'quantity',1))
    book.pages = int(get_POST_param(request,'pages',0))
    book.series = get_POST_param(request,'series')
    book.binding=get_POST_param(request,'binding')
    book.keywords=get_POST_param(request,'keywords')
    book.summary=get_POST_param(request,'summary')
    book.authorintro=get_POST_param(request,'authorintro')
    # book.status=book.status


def create_book(request):
        book=Book()
        fill_in_book(request,book)
        book_id = book_service.create_book(book)
        return HttpResponse("{'status':'OK','result':%d}" %book_id)

def update_book(request):
    bid = get_POST_param(request,'book_id',None)
    book = None
    if bid:
        book = book_service.get_book_by_id(bid)
    else:
        return HttpResponseServerError("id  is None")

    if not book:
        raise Http404("Book with id %s Not Found" % bid)

    fill_in_book(request,book)
    book_service.update_book(book)
    return HttpResponse("{'status':'OK'}")

# class BookListWrapper:
#     "For json serialization"
#     def __init__(self,blist,total_count=0,total_pages=0,npage=0):
#         "The item in blist should have a method named jsonable"
#         self.itemlist =[ sitem.jsonable() for sitem in blist ]
#         self.total = total_count
#         self.total_pages = total_pages
#         self.npage = npage
#
#     def jsonable(self):
#         return self.__dict__
