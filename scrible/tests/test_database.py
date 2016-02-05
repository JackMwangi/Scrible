import unittest

from ..notes import DatabaseManager
from ..notes import noteoperations

"""Unit tests for testing database NoteOperations
"""


class DbTests(unittest.TestCase):

    """Checks if can connect to a db
    """

    def test_connection(self):
        dbmgr = DatabaseManager.DatabaseManager("scribler.db")
        cursor = dbmgr.query("select COUNT(*) from notes")
        result = cursor.fetchone()
        rows = result[0]  # Type of rows should be integer
        self.assertEqual(type(rows), int)

    """ Tests whether an inserted record can be deleted
    """

    def test_delete(self):
        note = noteoperations.NoteOperations()
        note.save(title="testdelete", body="testrecorddelete")
        status = note.delete("", "all")
        self.assertGreater(status, 0)

    """ Tests whether an inserted record can be sought
    """

    def test_save(self):
        note = noteoperations.NoteOperations()
        note.save(title="testsave", body="testrecordsave")
        notes = note.search("testrecordsave", 1)
        bodynote = ""
        for item in notes:
            body = item.get("body", "")
            if body == "testrecordsave":
                bodynote = body
        self.assertEqual(bodynote, "testrecordsave")

    """ Tests whether an inserted record can be sought
    """

    def test_search(self):
        note = noteoperations.NoteOperations()
        note.save(title="testsearch", body="testrecordsearch")
        notes = note.search("testrecordsearch", 1)
        bodynote = ""
        for item in notes:
            body = item.get("body", "")
            if body == "testrecordsearch":
                bodynote = body
        self.assertEqual(bodynote, "testrecordsearch")
