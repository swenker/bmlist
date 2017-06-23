from django.http import HttpResponse, HttpResponseServerError
from django.http import JsonResponse
from django.http import Http404

from bmutils import PaginationListWrapper
from bmutils import get_GET_param
from bookcase.bookcase_service import *

# Create your views here.
CONTENT_TYPE = "application/json;charset=UTF-8"

"The api should be called within page instead of browser."

def __get_current_user():
    return 1

def create_bookcase():
    return


def get_bookcase(request):
    return JsonResponse('', content_type=CONTENT_TYPE)


def add_book_to_bookcase(request,book_id):

    bookcase_service.add_book(__get_current_user(),book_id)
    return HttpResponse("{'status':'OK'}")


def remove_book_from_bookcase(request, book_id):

    bookcase_service.remove_books(__get_current_user(), book_id)
    return HttpResponse("{'status':'OK'}")


def search_books(request):
    keyword = request.GET.get('k', None)
    npage = request.GET.get('np', 1)
    total_count, total_pages, book_list = bookcase_service.search_books(__get_current_user(),keyword, npage)
    if total_count:
        return JsonResponse(PaginationListWrapper(book_list, total_count, total_pages, npage).jsonable(),
                        content_type=CONTENT_TYPE)
    else:
        return HttpResponse("{'status':'NO'}")

def check_book_in_bookcase(request,book_id):
    in_bookcase = bookcase_service.get_book(__get_current_user(),book_id,None)
    if in_bookcase:
        return HttpResponse("{'status':'YES'}")
    else:
        return HttpResponse("{'status':'NO'}")