
from firebase import firebase
from clint.textui import colored, puts, indent, prompt
import getpass
import base64


class SyncNotes(object):
    def __init__(self, db):
        self.dbmgr = db
        try:
            self.fb = firebase.FirebaseApplication(
                'https://scrible.firebaseio.com', None)
        except Exception:
            puts(colored.red("Please check your internet connection"))

    def savenotestocloud(self, exists):
        if self.isuserindb():
            if self.arenotesindb():
                username = self.getusernamefromdb().get("username", "")
                passhash = self.getusernamefromdb().get("pass", "")
                if not self.isuserincloud(username):
                    self.saveuserincloud(username, passhash)
                    exists = "yes"
                notes = SyncNotes.fetchunsynced(self)
                if len(notes) > 0:
                    if exists == "yes":
                        self.fb.delete('/notes/' + username, None)
                        result = self.fb.post(
                            '/notes/' + username, notes)

                    else:
                        result = self.fb.post(
                            '/notes/' + username, notes)
                else:
                    self.fb.delete('/notes/' + username, None)
                with indent(4, quote=' >'):
                    puts(colored.green("Notes synced"))
                    self.flagsent()
            else:
                pass
                username = self.getusernamefromdb().get("username", "")
                passhash = self.getusernamefromdb().get("pass", "")
                if not self.isuserincloud(username):
                    self.saveuserincloud(username, passhash)
                    exists = "yes"
                self.getnotes(username)

        else:
            with indent(4, quote=' >'):
                puts(
                    colored.green("User account not found.Please create account"))
            name = prompt.query("Enter username")
            pswd = getpass.getpass('Enter password')
            self.createuser(name, pswd)

    def deletenotesfromcloud(self):
        self.fb.delete('/notes/' + self.getusernamefromdb().get("username", ""), None)

    def getnotes(self, user):
        username = self.getusernamefromdb().get("username", "")
        if username != "":
            notes = self.fb.get('/notes/' + user, None)
            listnotes = []
            if notes != None:
                for k, v in notes.iteritems():
                    listnotes = v
                for i in listnotes:
                    content = i.get("content")
                    title = content.get("title")
                    body = content.get("body")
                    self.savenotesindb(title=title, body=body)
                with indent(4, quote=' >'):
                    puts(colored.green("Notes synced"))
            else:
                with indent(4, quote=' >'):
                    puts(
                        colored.green("Sorry,no notes present found in the cloud"))
        else:
            pass
    def getreturnnotes(self, user):
        username = self.getusernamefromdb().get("username", "")
        if username != "":
            notes = self.fb.get('/notes/' + user, None)
            listnotes = []
            if notes != None:
                for k, v in notes.iteritems():
                    listnotes = v
                for i in listnotes:
                    content = i.get("content")
                    title = content.get("title")
                    body = content.get("body")
                    listnotes.append(title)
                return listnotes
                with indent(4, quote=' >'):
                    puts(colored.green("Notes synced"))
            else:
                with indent(4, quote=' >'):
                    puts(
                        colored.green("Sorry,no notes present found in the cloud"))
        else:
            pass

    def fetchunsynced(self):
        notescontent = []
        for row in self.dbmgr.query("select * from notes"):
            notetext = {}
            notetext["note_id"] = row[0]
            notetext["content"] = {'title': row[1], 'body': row[2]}
            notescontent.append(notetext)
        # print {'notes': notescontent}
        # return {'notes': notescontent}
        return notescontent

    def flagsent(self):
        for row in self.dbmgr.query("select * from notes where sent = 'NO'"):
            noteid = str(row[0])
            self.dbmgr.query(
                "update notes set sent = 'YES' where _id = '" + noteid + "'")

    def isuserindb(self):
        cursor = self.dbmgr.query("select COUNT(*) from users")
        result = cursor.fetchone()
        # print "num users " + str(result[0])
        if result[0] > 0:
            return True
        return False

    def getuserpassfromcloud(self, user):
        try:
            result = self.fb.get('/users/' + user, None)
        except Exception:
            puts(colored.red("Please check your internet connection"))
        return result

    def getusernamefromdb(self):
        name = {}
        for row in self.dbmgr.query("select * from users limit 1"):
            name["username"] = row[1]
            name["pass"] = row[2]
        return name

    def isuserincloud(self, user):
        try:
            result = self.fb.get('/users', user)
            if result != None:
                return True
            return False
        except Exception:
            puts(colored.red("Please check your internet connection"))
            exit()
            

    def arenotesindb(self):
        cursor = self.dbmgr.query("select COUNT(*) from notes")
        result = cursor.fetchone()
        # print "num notes " + str(result[0])
        if result[0] > 0:
            return True
        return False

    def saveuserincloud(self, username, passhash):
        try:
            result = self.fb.post(
                '/users/' + username, passhash)
        except Exception:
            puts(colored.red("Please check your internet connection"))
        with indent(4, quote=' >'):
            puts(colored.green("User saved in cloud"))

    def savenotesindb(self, **content):
        title = ""
        body = ""
        if len(content) == 2:
            # Both title and content exist
            title = content['title']
            body = content['body']
        elif len(content) == 1:
            title = content['title']
        self.dbmgr.query(
            "insert into notes(Title,Content,sent) VALUES('" + title + "','" + body + "','NO')")

    def createuser(self, username, password):
        passhash = base64.b64encode(password)
        if not self.isuserincloud(username):
            created = self.dbmgr.query(
                "insert into users(username,passhash,active) VALUES('" + username + "','" + passhash + "','YES')")
            if created > 0:
                self.saveuserincloud(username, passhash)
                with indent(4, quote=' >'):
                    puts(colored.green("User created"))
            self.savenotestocloud("no")
        else:
            pwdict = self.getuserpassfromcloud(username)
            for key, value in pwdict.iteritems():
                pwd = value
            created = self.dbmgr.query(
                "insert into users(username,passhash,active) VALUES('" + username + "','" + pwd + "','YES')")
            self.savenotestocloud("yes")
