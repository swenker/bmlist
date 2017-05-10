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

    #web UI goes here
    url(r'^list$',views.list,name='a_list'),
    url(r'^add$',views.new_commnet,name='new_commnet'),

    #API goes here
    url(r'^api/search', api_views.search_comment, name='api_comment_list'),
    url(r'^api/rm/(?P<cid>[0-9]+)$',api_views.delete_comment, name='api_delete_comment'),
    url(r'^api/add',api_views.new_comment, name='api_new_comment'),
]