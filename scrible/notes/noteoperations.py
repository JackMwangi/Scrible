from DatabaseManager import DatabaseManager
from ..sync import cloudsync
import time

class NoteOperations(object):
    dbmgr = None

    def __init__(self):
        self.dbmgr = DatabaseManager("scribler.db")

    def save(self, **content):
        title = ""
        body = ""
        if len(content) == 2:
            # Both title and content exist
            title = content['title']
            body = content['body']
        elif len(content) == 1:
            title = content['title']
        self.dbmgr.query(
            "insert into notes(Title,Content,sent,datecreated) VALUES('" + title + "','" + body + "','NO','"+self.gettime()+"')")

    def view(self, noteid=""):
        notetext = {}
        dbmgr = DatabaseManager("scribler.db")
        for row in dbmgr.query("select * from notes where _id = '" + noteid + "'"):
            notetext["title"] = row[1]
            notetext["body"] = row[2]
        return notetext

    def delete(self, noteid="",allnotes = "one"):
        dbmgr = DatabaseManager("scribler.db")
        if allnotes == "one" :
            print "onenote"
            status = dbmgr.query("delete from notes where _id = '" + noteid + "'")
        else:
            print "allnotes"
            status = dbmgr.query("delete from notes")
            print status.rowcount
        return status.rowcount

    def getnotetitle(self, noteid=""):
        dbmgr = DatabaseManager("scribler.db")
        for row in dbmgr.query("select * from notes where _id = '" + noteid + "'"):
            return row[1]

    def synctocloud(self):

        dbmgr = DatabaseManager("scribler.db")
        sy = cloudsync.SyncNotes(dbmgr)
        sy.savenotestocloud("yes")

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

        return listtext

    def gettime(self):
        localtime   = time.localtime()
        timeString  = time.strftime("%H:%M %d/%m/%Y", localtime)
        return timeString

    def search(self, query="", limit=1):
        listtext = []
        dbmgr = DatabaseManager("scribler.db")
        if limit == 1:
            for row in dbmgr.query("select * from notes where title LIKE '%" + query + "%' or content LIKE '%" + query + "%'"):
                notetext = {}
                notetext["title"] = row[1]
                notetext["body"] = row[2]
                listtext.append(notetext)
        elif limit > 1:
            for row in dbmgr.query("select * from notes where title LIKE '%" + query + "%' or content LIKE '%" + query + "%' limit '" + str(limit) + "'"):
                notetext = {}
                notetext["title"] = row[1]
                notetext["body"] = row[2]
                listtext.append(notetext)

        return listtext
