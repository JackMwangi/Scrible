from DatabaseManager import DatabaseManager
from ..sync import cloudsync
import time

"""This class provides methods for easy database operations
"""


class NoteOperations(object):
    dbmgr = None

    def __init__(self):  # constructor initiates database connection instance
        self.dbmgr = DatabaseManager("scribler.db")

        """Performs insert in db to save a notetext
        """

    def save(self, **content):  # content contains the body and title of a note
        title = ""
        body = ""
        if len(content) == 2:
            # Both title and content exist
            title = content['title']
            body = content['body']
        elif len(content) == 1:  # only title exists
            title = content['title']
        # save to db
        self.dbmgr.query(
            "insert into notes(Title,Content,sent,datecreated) VALUES('" + title + "','" + body + "','NO','" + self.gettime() + "')")

    """Retrieves a single note from db using the note id.Returns
        the note as a dicts
    """

    def view(self, noteid=""):
        notetext = {}
        dbmgr = DatabaseManager("scribler.db")
        for row in dbmgr.query("select * from notes where _id = '" + noteid + "'"):
            notetext["title"] = row[1]
            notetext["body"] = row[2]
        return notetext

    """Deletes a single note from db using the note id or all notes when specified.
        Returns the number of rows affected.
    """

    def delete(self, noteid="", allnotes="one"):
        dbmgr = DatabaseManager("scribler.db")
        if allnotes == "one":
            status = dbmgr.query(
                "delete from notes where _id = '" + noteid + "'")
        else:
            status = dbmgr.query("delete from notes")
        return status.rowcount

    """Returns the note title using the note id supplied
    """

    def getnotetitle(self, noteid=""):
        dbmgr = DatabaseManager("scribler.db")
        for row in dbmgr.query("select * from notes where _id = '" + noteid + "'"):
            return row[1]

    """Performs synchronization of notes to and from the cloud and local database
    """

    def synctocloud(self):
        dbmgr = DatabaseManager("scribler.db")
        # cloudsync responsible for synchronization
        sy = cloudsync.SyncNotes(dbmgr)
        sy.savenotestocloud("yes")

    """Deletes a note all notes of a user in the cloud
        when the user deletes all notes at once locally.
    """

    def deletenotesfromcloud(self):
        dbmgr = DatabaseManager("scribler.db")
        sy = cloudsync.SyncNotes(dbmgr)
        sy.deletenotesfromcloud()

    """Returns all notes in the local db.Returns a specific
        number of notes if limit parameter is specified and all notes if the limit 
        is not specified
    """

    def viewall(self, limit=1):
        listtext = []
        dbmgr = DatabaseManager("scribler.db")
        if limit == 1:
            for row in dbmgr.query("select * from notes"):
                notetext = {}
                notetext["_id"] = row[0]
                notetext["title"] = row[1]
                notetext["body"] = row[2]
                notetext["datecreated"] = row[4]
                listtext.append(notetext)
        elif limit > 1:

            for row in dbmgr.query("select * from notes limit '" + str(limit) + "'"):
                notetext = {}
                notetext["_id"] = row[0]
                notetext["title"] = row[1]
                notetext["body"] = row[2]
                notetext["datecreated"] = row[4]
                listtext.append(notetext)

        return listtext  # list containing dictionary entries of notes

    """Like `viewall`,it returns a list of notes when `next` is invoked
        by skipping the rows already queried
    """

    def viewallskip(self, limit=1, offset=1):
        listtext = []
        dbmgr = DatabaseManager("scribler.db")
        if limit == 1:
            for row in dbmgr.query("select * from notes"):
                notetext = {}
                notetext["_id"] = row[0]
                notetext["title"] = row[1]
                notetext["body"] = row[2]
                notetext["datecreated"] = row[4]
                listtext.append(notetext)
        elif limit > 1:
            for row in dbmgr.query("select * from notes limit '" + str(limit) + "' OFFSET '" + str(offset) + "'"):
                notetext = {}
                notetext["_id"] = row[0]
                notetext["title"] = row[1]
                notetext["body"] = row[2]
                notetext["datecreated"] = row[4]
                listtext.append(notetext)

        return listtext

    """Returns the local time that is added as a note metadata for the creation datecreated
    """

    def gettime(self):
        localtime = time.localtime()
        timeString = time.strftime("%H:%M %d/%m/%Y", localtime)
        return timeString

    """Queries the db for notes containing the string specified and returns a list
        of the notes.
    """

    def search(self, query="", limit=1):
        listtext = []
        dbmgr = DatabaseManager("scribler.db")
        if limit == 1:
            for row in dbmgr.query("select * from notes where title LIKE '%" + query + "%' or content LIKE '%" + query + "%'"):
                notetext = {}
                notetext["_id"] = row[0]
                notetext["title"] = row[1]
                notetext["body"] = row[2]
                notetext["datecreated"] = row[4]
                listtext.append(notetext)
        elif limit > 1:
            for row in dbmgr.query("select * from notes where title LIKE '%" + query + "%' or content LIKE '%" + query + "%' limit '" + str(limit) + "'"):
                notetext = {}
                notetext["_id"] = row[0]
                notetext["title"] = row[1]
                notetext["body"] = row[2]
                notetext["datecreated"] = row[4]
                listtext.append(notetext)

        return listtext

    """Like `search`,it returns a list of notes matching query string when `next` is invoked
        by skipping the rows already queried
    """

    def searchskip(self, query="", limit=1, offset=1):
        listtext = []
        dbmgr = DatabaseManager("scribler.db")
        if limit == 1:
            for row in dbmgr.query("select * from notes where title LIKE '%" + query + "%' or content LIKE '%" + query + "%'"):
                notetext = {}
                notetext["_id"] = row[0]
                notetext["title"] = row[1]
                notetext["body"] = row[2]
                notetext["datecreated"] = row[4]
                listtext.append(notetext)
        elif limit > 1:
            for row in dbmgr.query("select * from notes where title LIKE '%" + query + "%' or content LIKE '%" + query + "%' limit '" + str(limit) + "' OFFSET '" + str(offset) + "'"):
                notetext = {}
                notetext["_id"] = row[0]
                notetext["title"] = row[1]
                notetext["body"] = row[2]
                notetext["datecreated"] = row[4]
                listtext.append(notetext)

        return listtext
