
from firebase import firebase
from clint.textui import colored, puts, indent, prompt
import getpass
import base64
import time
import sys
import threading
from colorama import Fore, Back, Style

"""Class for all synchronization operations between local
    database and online Firebase db
"""


class SyncNotes(object):

    def __init__(self, db):  # initiates Firebase class
        self.done = False
        self.dbmgr = db
        try:
            self.fb = firebase.FirebaseApplication(
                'https://scrible.firebaseio.com', None)
        except Exception:
            puts(colored.red("Please check your internet connection"))

    """Does saving notes to server and fetching from server into local db
    """

    def savenotestocloud(self, exists):
        # if there is a user present in local db proceed wih sync
        if self.isuserindb():

            # Creates a thread class and starts it that does progress
            # animations while synchronizing
            p = progress_bar_loading()
            p.start()
            # if there are notes present in the db,sync the notes
            try:
                if self.arenotesindb():
                    username = self.getusernamefromdb().get("username", "")
                    passhash = self.getusernamefromdb().get("pass", "")
                    if not self.isuserincloud(username):
                        self.saveuserincloud(username, passhash)
                        exists = "yes"
                    # gets a list of notes from db
                    notes = SyncNotes.fetchunsynced(self)
                    if len(notes) > 0:
                        if exists == "yes":
                            # deletes first the data,then inserts so as to update
                            # it
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
                        p.stopit()

                        self.flagsent()  # flags notes as sent
                else:  # else fetch notes from the cloud and insert to local db
                    username = self.getusernamefromdb().get("username", "")
                    passhash = self.getusernamefromdb().get("pass", "")
                    if not self.isuserincloud(username):
                        self.saveuserincloud(username, passhash)
                        exists = "yes"
                    self.getnotes(username)
            except:
                p.stopit()


        else:  # Else create the user account and try to sync again
            with indent(4, quote=' >'):
                puts(
                    colored.red("User account not found.Please create account"))
            name = prompt.query("Enter username")
            pswd = getpass.getpass('Enter password')
            self.createuser(name, pswd)

    def deletenotesfromcloud(self):
        self.fb.delete(
            '/notes/' + self.getusernamefromdb().get("username", ""), None)

    """This retrieves the notes from the cloud
     using the username and saves them
     """

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
                        colored.red("Sorry,no notes present found in the cloud"))
        else:
            pass  # to do later

    """This retrieves the notes from the cloud
     using the username and returns them to calling function
     """

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
                        colored.red("Sorry,no notes present found in the cloud"))
        else:
            pass

    """Gets a list of records from db for synchronization
    """

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
    """Flags notes as sent by updating
    """

    def flagsent(self):
        for row in self.dbmgr.query("select * from notes where sent = 'NO'"):
            noteid = str(row[0])
            self.dbmgr.query(
                "update notes set sent = 'YES' where _id = '" + noteid + "'")

    """Checks if there is a user in local db
    """

    def isuserindb(self):
        cursor = self.dbmgr.query("select COUNT(*) from users")
        result = cursor.fetchone()
        # print "num users " + str(result[0])
        if result[0] > 0:
            return True
        return False
    """Gets hashed password from server of a user account
    """

    def getuserpassfromcloud(self, user):
        try:
            result = self.fb.get('/users/' + user, None)
        except Exception:
            puts(colored.red("Please check your internet connection"))
        return result

    """Returns the name of the user from local db
    """

    def getusernamefromdb(self):
        name = {}
        for row in self.dbmgr.query("select * from users limit 1"):
            name["username"] = row[1]
            name["pass"] = row[2]
        return name

    """Checks whether the user supplied is saved in the cloud
    """

    def isuserincloud(self, user):
        try:
            result = self.fb.get('/users', user)
            if result != None:
                return True
            return False
        except Exception:
            puts(colored.red("Please check your internet connection"))
            exit()

    """Checks whether any notes are present in local db
    """
    def arenotesindb(self):
        cursor = self.dbmgr.query("select COUNT(*) from notes")
        result = cursor.fetchone()
        # print "num notes " + str(result[0])
        if result[0] > 0:
            return True
        return False

        """saves a user account to Firebase
        """
    def saveuserincloud(self, username, passhash):
        try:
            result = self.fb.post(
                '/users/' + username, passhash)
        except Exception:
            puts(colored.red("Please check your internet connection"))
        with indent(4, quote=' >'):
            puts(colored.green("User saved in cloud"))

    """saves notes to local db
    """
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

    """creates a user account in local db if the account is not in the cloud.
       Then creates the same in firebase and uploads notes
    """
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

"""Thread class to run synchronizing animation on a separate thread
"""


class progress_bar_loading(threading.Thread):
    def run(self):
        self.kill = False
        self.stop = False
        # print 'Synchronizing....  ',
        print(Fore.YELLOW + 'Synchronizing....  '),
        sys.stdout.flush()
        i = 0
        while self.stop != True: # execute while stop vaiable is false
            if (i % 4) == 0:
                sys.stdout.write('\b/')
            elif (i % 4) == 1:
                sys.stdout.write('\b-')
            elif (i % 4) == 2:
                sys.stdout.write('\b\\')
            elif (i % 4) == 3:
                sys.stdout.write('\b|')
            sys.stdout.flush()
            time.sleep(0.2)
            i += 1

    def stopit(self):
        self.stop = True #set stop to true to stop while loop execution
