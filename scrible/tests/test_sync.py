import unittest

from ..notes import DatabaseManager
from ..notes import noteoperations
from ..sync import cloudsync
from firebase import firebase


class SyncTest(unittest.TestCase):

    def getusername(self,user):
        self.fb = firebase.FirebaseApplication(
                'https://scrible.firebaseio.com', None)
        result = self.fb.get('/users', user)
        if result != None:
            return True
        return False

    def test_saveusercloud(self):
        dbmgr = DatabaseManager.DatabaseManager("scribler.db")
        sync = cloudsync.SyncNotes(dbmgr)
        sync.saveuserincloud("test", "45FG~~")
        self.assertEqual(self.getusername("test"), True)

    def test_savenotestocloud(self):
        note = noteoperations.NoteOperations()
        note.save(title="testsavecloud", body="testsavecloud")
        dbmgr = DatabaseManager.DatabaseManager("scribler.db")
        sync = cloudsync.SyncNotes(dbmgr)
        sync.savenotestocloud("yes")
        noteslist = sync.getreturnnotes("test")
        titletest = ""
        for title in noteslist:
            if title == "testsavecloud":
                titletest = title
        self.assertEqual(titletest, "testsavecloud")
