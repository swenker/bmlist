from django.core.paginator import Paginator
from django.db.models import Q

from xnote.models import XNote


class XNoteService():
    def search_notes(self, uid, keyword=None, npage=1):
        total_count = 0
        total_pages = 0
        N_EVERY_PAGE = 2
        if keyword:
            note_list = XNote.objects.filter(uid=uid) \
                .filter(Q(title__icontains=keyword) | Q(content__icontains=keyword)) \
                .order_by('-update_time')
        else:
            note_list = XNote.objects.filter(uid=uid).order_by('-update_time')

        total_count = len(note_list)
        total_pages = (total_count + N_EVERY_PAGE - 1) / N_EVERY_PAGE

        paginator = Paginator(note_list, N_EVERY_PAGE)
        note_list = paginator.page(npage)

        return total_count, total_pages, note_list

    def save_notes(self, note):
        note.save()

    def load_note(self, note_id):
        try:
            return XNote.objects.get(id=note_id)
        except XNote.DoesNotExist, dne:
            return None

    def delete_note(self, note_id):
        try:
            note = XNote.objects.get(id=note_id)
            note.delete()
            return True
        except XNote.DoesNotExist, dne:
            return None
