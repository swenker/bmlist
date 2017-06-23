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
    url(r'^book/list$', views.list_books, name='list_books'),

    #API goes here
    url(r'^api/book/search', api_views.search_books, name='api_search_list'),
    url(r'^api/book/list',api_views.search_books, name='api_list_book'),
    url(r'^api/book/add/(?P<book_id>[0-9]+)$',api_views.add_book_to_bookcase, name='api_add_book'),
    url(r'^api/book/rm/(?P<book_id>[0-9]+)$',api_views.add_book_to_bookcase, name='api_rm_book'),
    url(r'^api/book/check/(?P<book_id>[0-9]+)$',api_views.check_book_in_bookcase, name='api_check_book'),
]