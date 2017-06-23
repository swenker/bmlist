from django.shortcuts import render
from bmutils import *
# Create your views here.

def index(request):
    context ={ 'abc':'1234567890'}
    return render(request,'books/index.html',context)

def list(request):
    keyword = get_GET_param(request,'k','')
    npage = get_GET_param(request,'np',1)
    context={'keyword':keyword,"npage":npage}
    return render(request,'books/book_list.html',context)

def get_book_by_id(request,book_id):
    context={'book_id':book_id}
    return render(request,'books/book_view.html',context)

def edit_book_form_by_id(request,book_id):
    "The parameter is still in string format instead of int"
    context={'book_id':book_id}
    return render(request,'books/book_form.html',context)

def new_book_form(request):
    return render(request,'books/book_form.html')

def delete_book(request,book_id):
    pass

def get_book_by_isbn(request,isbn):
    "search it locally,if not found then try to get it from remote service"
    context={'isbn':isbn}
    return render(request,'books/book_view.html',context)

def search_book_by_isbn_for_add(request,isbn=None):
    "search it locally,if not found then try to get it from remote service"
    context={'isbn':isbn}
    return render(request,'books/book_search_isbn.html',context)

def get_param(request, param_name, default_value=None):
    return request.GET.get(param_name,default_value)


