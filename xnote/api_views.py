from django.http import HttpResponse, HttpResponseServerError
from django.http import JsonResponse
from django.http import Http404

from bmutils import *
from xnote.XNoteService import XNoteService
from xnote.models import XNote

CONTENT_TYPE="application/json;charset=UTF-8"

xnote_service = XNoteService()
def list_notes(request):

    npage = get_GET_param(request,'np',1)
    uid = 1
    total_count, total_pages, note_list = xnote_service.search_notes(uid,keyword=None,npage=npage)

    return JsonResponse( PaginationListWrapper(note_list, total_count, total_pages, npage).jsonable(),content_type=CONTENT_TYPE)

def search_notes(request):
    keyword = get_GET_param(request,'k','')
    npage = get_GET_param(request,'np',1)
    uid = 1
    total_count, total_pages, note_list = xnote_service.search_notes(uid,keyword=keyword,npage=npage)
    # return HttpResponse(book.jsonable(),content_type="application/json")

    return JsonResponse( PaginationListWrapper(note_list, total_count, total_pages, npage).jsonable(),content_type=CONTENT_TYPE)

def export_notes(request):
    keyword = ''
    uid = 1
    total_count, total_pages, note_list = xnote_service.search_notes(uid,keyword=keyword,npage=None)
    return JsonResponse( PaginationListWrapper(note_list, total_count, total_pages, 0).jsonable(),content_type=CONTENT_TYPE)


def get_note_by_id(request,note_id):
    note  = xnote_service.load_note(note_id)
    if note:
        json_response = JsonResponse(note.jsonable(),content_type=CONTENT_TYPE)
        # json_response._headers['X-Frame-Options']='*'
        return json_response
    else:
        raise Http404("Note with id %s Not Found" % id)

def delete_note(request,note_id):
    if not xnote_service.delete_note(note_id):
        raise Http404("Note with id %s Not Found" % note_id)
    return HttpResponse("{'status':'OK'}")

def save_note(request):
    note_id = get_POST_param(request,'note_id')
    if note_id:
        note = xnote_service.load_note(note_id)
    else:
        note = XNote()
        note.create_time = get_now()

        #TODO
        note.uid=1
    try:
        note.title = get_POST_param(request,'title')
        note.content = get_POST_param(request,'content')
        note.update_time = get_now()
        xnote_service.save_notes(note)
        return HttpResponse('{"note_id":%d}'%note.id,content_type=CONTENT_TYPE)

    except AttributeError,be:
        print be
        return JsonResponse(be.message)





