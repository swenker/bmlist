from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,"xnote/index.html")

def list_notes(request):
    return render(request,'xnote/notes_list.html')

def new_note(request):
    return render(request,'xnote/note_form.html')

def edit_note(request,note_id):
    context = {'note_id':note_id}
    return render(request,'xnote/note_form.html',context)





