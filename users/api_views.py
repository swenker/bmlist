from django.shortcuts import render
from django.http import HttpResponse, HttpResponseServerError
from django.http import JsonResponse
from django.http import Http404

from bmlist_service import user_service
from users.models import *
from bmutils import PaginationListWrapper

# Create your views here.
CONTENT_TYPE="application/json;charset=UTF-8"

def search_account(request):
    keyword = request.GET.get('k',None)
    npage = request.GET.get('np',1)
    total_count,total_pages,account_list = user_service.search_accounts(keyword,npage)
    # return HttpResponse(book.jsonable(),content_type="application/json")

    return JsonResponse( PaginationListWrapper(account_list, total_count, total_pages, npage).jsonable(),content_type=CONTENT_TYPE)

def get_account_by_id(request,account_id):
    "The parameter is still in string format instead of int"
    account = user_service.get_user_by_id(account_id)
    if not account:
        raise Http404("User with id %s Not Found" % account_id)

    return JsonResponse(account.jsonable())

def get_account_by_email(request,email):
    account  = user_service.get_user_by_email(email)
    if account:
        json_response = JsonResponse(account.jsonable(),content_type=CONTENT_TYPE)
        # json_response._headers['X-Frame-Options']='*'
        return json_response
    else:
        raise Http404("User with email %s Not Found" % email)

def delete_account(request,account_id):
    if not user_service.delete_user(account_id):
        raise Http404("User with id %s Not Found" % account_id)

    return HttpResponse("{'status':'OK'}")


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


def __fill_in_account(request,account):
    account.email = get_POST_param(request, 'email')
    account.passwd = get_POST_param(request, 'passwd')
    account.nickname = get_POST_param(request, 'nickname')

def signup(request):
    account = Account()

    __fill_in_account(request,account)

def signin(request):
    passwd = get_POST_param(request, 'passwd')
    login_id = get_POST_param(request, 'login_id')

    user_service.signin(passwd,login_id)


