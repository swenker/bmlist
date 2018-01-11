from django.core.paginator import Paginator
from django.db.models import Q

from xnote.models import XNote


class XNoteService():
    def search_notes(self, uid, keyword=None, npage=1):
        total_count = 0
        total_pages = 0
        N_EVERY_PAGE = 5
        common_filter = XNote.objects.filter(uid=uid)
        if keyword:
            note_list = common_filter.filter(Q(title__icontains=keyword) | Q(content__icontains=keyword)) \
                .order_by('-update_time')
        else:
            note_list = common_filter.order_by('-update_time')

        if npage:
            total_count = len(note_list)
            total_pages = (total_count + N_EVERY_PAGE - 1) / N_EVERY_PAGE

            paginator = Paginator(note_list, N_EVERY_PAGE)
            # print("npages:%d" %npage)
            note_list = paginator.page(npage)

            return total_count, total_pages, note_list
        else:
            #return all the items if no npage is given? TODO
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
