from django.shortcuts import render

# Create your views here.

def add(request):
    # context = {'keyword': keyword, "npage": npage}
    return render(request, 'users/account_list.html')


def list(request):
    return render(request,'comment_list.html')

