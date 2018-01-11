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
    url(r'^list$',views.list_notes,name='list_notes'),
    url(r'^edit/(?P<note_id>[0-9]+)$',views.edit_note,name='edit'),
    url(r'^add$',views.new_note,name='edit'),
    # url(r'^edit/(?P<account_id>[0-9]+)$',views.edit_note,name='edit'),

    #API goes here
    url(r'^api/list$', api_views.list_notes, name='api_list_notes'),
    url(r'^api/search$', api_views.search_notes, name='api_search_notes'),
    url(r'^api/export$', api_views.export_notes, name='api_export_notes'),

    #the P name should be the same as those in the method signature
    url(r'^api/detail/(?P<note_id>[0-9]+)$', api_views.get_note_by_id, name='get_note_by_id'),
    url(r'^api/rm/(?P<note_id>[0-9]+)$',api_views.delete_note, name='api_delete_note'),
    url(r'^api/save$',api_views.save_note, name='api_save'),
]