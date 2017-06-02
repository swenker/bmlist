from django.shortcuts import render


# Create your views here.

def index(request):
    context = {'abc': '1234567890'}
    return render(request, 'books/index.html', context)


def list(request):
    keyword = request.GET.get('k', '')
    npage = request.GET.get('np', 1)
    context = {'keyword': keyword, "npage": npage}
    return render(request, 'users/user_list.html', context)


def get_account_by_id(request, account_id):
    context = {'account_id': account_id}
    return render(request, 'users/account_view.html', context)


def signup(request):
    return render(request, 'users/signup.html')


def signin(request):
    return render(request, 'users/signin.html')


def get_param(request, param_name, default_value=None):
    return request.GET.get(param_name, default_value)
