__author__ = 'wenjusun'

from django.conf.urls import url

from . import views
from . import api_views

"""
In Python regular expressions,
the syntax for named regular-expression groups is (?P<name>pattern),
where name is the name of the group and pattern is some pattern to match.
"""
urlpatterns = [
    url(r'^$', views.index, name='index'),

    #web UI goes here
    url(r'^list$',views.list,name='user_list'),
    url(r'^detail/(?P<account_id>[0-9]+)$',views.get_account_by_id,name='account_detail_id'),
    url(r'^signup$',views.signup,name='signup'),

    #API goes here
    url(r'^api/search', api_views.search_account, name='api_book_list'),
    url(r'^api/detail/(?P<book_id>[0-9]+)$', api_views.get_book_detail, name='api_book_detail'),
    url(r'^api/rm/(?P<book_id>[0-9]+)$',api_views.delete_book, name='api_delete_book'),
    url(r'^api/signup',api_views.signup, name='api_create_book'),
    url(r'^api/update$',api_views.update_book, name='api_update_book'),
]