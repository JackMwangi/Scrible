from DatabaseManager import DatabaseManager


class NoteOperations(object):
    dbmgr = None

    def __init__(self):
        self.dbmgr = DatabaseManager("scribler.db")

    def save(self, **content):
        title = ""
        body = ""
        if len(content) == 2:
            #Both title and content exist
            title = content['title']
            body = content['body']
        elif len(content) == 1:
            if ('title' in content):
                print content['title']
                title = content['title']
            else:
                print content['body']
                body = content['body']

        self.dbmgr.query(
            "insert into notes(Title,Content) VALUES('" + title + "','" + body + "')")

    def view(self, noteid=""):
        pass
