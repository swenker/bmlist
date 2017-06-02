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
    url(r'^signin$',views.signin,name='signin'),

    #API goes here
    url(r'^api/search', api_views.search_account, name='api_account_list'),
    url(r'^api/detail/(?P<account_id>[0-9]+)$', api_views.get_account_by_id, name='api_account_detail'),
    url(r'^api/rm/(?P<book_id>[0-9]+)$',api_views.delete_account, name='api_delete_account'),
    url(r'^api/signup',api_views.signup, name='api_signup'),
    url(r'^api/signin',api_views.signin, name='api_signin'),
]