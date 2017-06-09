from django.test import TestCase

# Create your tests here.
from xnote.XNoteService import XNoteService
from xnote.models import XNote
import django.middleware.clickjacking.py

class XNoteTest(TestCase):
    def test_save_note(self):
        note = XNote()
        xnote_service = XNoteService()
        note.title='I am a test'
        xnote_service.save_notes(note)
        print note.id

        print xnote_service.search_notes(1,npage=1)