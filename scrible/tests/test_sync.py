import unittest

from ..notes import DatabaseManager
from ..notes import noteoperations
from ..sync import cloudsync
from firebase import firebase

"""Unit tests for testing synchronization operations
"""


class SyncTest(unittest.TestCase):

    """return True if the supplied username is found
        in Firebase
    """
    def getusername(self, user):
        self.fb = firebase.FirebaseApplication(
                'https://scrible.firebaseio.com', None)
        result = self.fb.get('/users', user)
        if result != None:
            return True
        return False

    """checks if the crested user has been sychronized with Firebase
    """
    def test_saveusercloud(self):
        dbmgr = DatabaseManager.DatabaseManager("scribler.db")
        sync = cloudsync.SyncNotes(dbmgr)
        sync.saveuserincloud("test", "45FG~~")
        self.assertEqual(self.getusername("test"), True)

    """checks if the crested note has been sychronized with Firebase
    """
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
