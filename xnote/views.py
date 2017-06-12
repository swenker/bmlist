from django.shortcuts import render

# Create your views here.
from bmutils import get_GET_param


def index(request):
    return render(request,"xnote/index.html")

def list_notes(request):
    keyword = get_GET_param(request,'k','')
    npage = get_GET_param(request,'np',1)

    context={'k':keyword,'np':npage}
    return render(request,'xnote/notes_list.html',context)

def new_note(request):
    return render(request,'xnote/note_form.html')

def edit_note(request,note_id):
    context = {'note_id':note_id}
    return render(request,'xnote/note_form.html',context)





