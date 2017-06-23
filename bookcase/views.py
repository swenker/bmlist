from django.shortcuts import render
from bmutils import *

# Create your views here.
def index(request):
    return render(request, 'bookcase/index.html')

def list_books(request):
    keyword = get_GET_param(request,'k','')
    npage = get_GET_param(request,'np',1)

    context = {'keyword':keyword,'npage':npage}

    return render(request,'bookcase/book_list.html',context = context)

def create_bookcase():
    return

def get_bookcase(request):
    # context = {'account_id': account_id}
    return render(request, 'bookcase_view.html')


def add_book_to_bookcase(request):
    return ''


def remove_book_from_bookcase(request, shelf_id):
    return ''

