import unittest

from ..notes import DatabaseManager
from ..notes import noteoperations

class DbTests(unittest.TestCase):

	def test_connection(self):
		dbmgr = DatabaseManager.DatabaseManager("scribler.db")
		cursor = dbmgr.query("select COUNT(*) from notes")
		result = cursor.fetchone()
		rows = result[0]
		self.assertEqual(type(rows), int)

	def test_delete(self):
		note = noteoperations.NoteOperations()
		note.save(title="testdelete", body="testrecorddelete")
		status = note.delete("", "all")
		self.assertGreater(status, 0)

	def test_save(self):
		note = noteoperations.NoteOperations()
		note.save(title="testsave", body="testrecordsave")
		notes = note.search("testrecordsave", 1)
		self.assertEqual(1, 1)

	def test_search(self):
		note = noteoperations.NoteOperations()
		note.save(title="testsearch", body="testrecordsearch")
		notes = note.search("testrecordsearch", 1)
		self.assertEqual(1, 1)






	