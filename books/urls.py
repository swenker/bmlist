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
    url(r'^list$',views.list,name='book_list'),
    url(r'^detail/(?P<book_id>[0-9]+)$',views.get_book_by_id,name='book_detail_id'),
    url(r'^edit/(?P<book_id>[0-9]+)$',views.edit_book_form_by_id,name='book_form_id'),
    url(r'^newbook$',views.new_book_form,name='book_form_id'),
    url(r'^isbn/(?P<isbn>[0-9]{10,13})$',views.get_book_by_isbn,name='get_by_isbn'),
    url(r'^risbn/([0-9]{10,13})$',views.search_book_by_isbn_for_add,name='get_by_isbn_add'),
    url(r'^risbn/?$',views.search_book_by_isbn_for_add,name='get_by_isbn_add'),

    #API goes here
    url(r'^api/search', api_views.search_book, name='api_book_list'),
    url(r'^api/detail/(?P<book_id>[0-9]+)$', api_views.get_book_detail, name='api_book_detail'),
    url(r'^api/rm/',api_views.delete_book, name='api_delete_book'),
    url(r'^api/create$',api_views.create_book, name='api_create_book'),
    url(r'^api/update$',api_views.update_book, name='api_update_book'),
    url(r'^api/add/',api_views.add_book_to_user_shelf,name='api_add_book'),
    url(r'^api/isbn/(?P<isbn>[0-9]{10,13})$',api_views.get_book_by_isbn,name='api_get_by_isbn'),
    url(r'^api/risbn/(?P<isbn>[0-9]{10,13})$',api_views.get_book_by_isbn_for_add,name='api_get_by_isbn_add'),
]