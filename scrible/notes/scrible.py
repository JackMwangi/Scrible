#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This shows the usage and options that available for the Scrible note taking app
Usage:
    scrible createnote  (<note_title>) [-m]
    scrible viewnote    (<note_id>) [-m]
    scrible deletenote  (<note_id> | -a)
    scrible searchnotes (<query_string>) [(--limit <items>)]
    scrible viewnote    (<note_id>)
    scrible listnotes   [(--limit <items>)]
    scrible next
    scrible export      (<filename>)
    scrible import      (<filename>)
    scrible sync [<direction>]
    scrible (-s | --start)
    scrible (-h | --help | --version)
Options:
    -s, --start  Interactive Mode
    -h, --help  Show this screen and exit.
    -m          Starts creating note body
"""

import sys
import csv
import os
import cmd
from docopt import docopt, DocoptExit
from noteoperations import NoteOperations
from clint.textui import colored, puts, indent
from colorama import init
from termcolor import cprint
from pyfiglet import figlet_format
from colorama import init, Fore, Back, Style


# compares the arguments to determine if all have been entered in correct
# manner
def parser(func):

    def fn(self, arg):
        try:
            # tries to compare entered commands against the doc
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The entered arguments don't match

            print('Sorry,you entered an invalid command')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn

"""Class overrides method parser so as to validate input.The input arguments
    are mapped to respective methods
"""


class Scrible (cmd.Cmd):

    # intro = 'Welcome to Scrible NoteApp!' \
    #     + ' (type help for a list of commands.)'
    
    prompt = '(Scrible) '
    file = None

    @parser
    def do_createnote(self, arg):
        """Usage: createnote  (<note_title>) [-m]"""

        createnewnote(arg)

    @parser
    def do_viewnote(self, arg):
        """Usage: viewnote    (<note_id>) [-m]"""

        viewsinglenote(arg)

    @parser
    def do_deletenote(self, arg):
        """Usage: deletenote  (<note_id> | -a)"""

        deletenote(arg)

    @parser
    def do_searchnotes(self, arg):
        """Usage: searchnotes (<query_string>) [(--limit <items>)]"""

        searchnotes(arg)

    @parser
    def do_listnotes(self, arg):
        """Usage: listnotes   [(--limit <items>)]"""

        listnotes(arg)

    @parser
    def do_sync(self, arg):
        """Usage: sync [<direction>]"""

        synctocloud(arg)

    @parser
    def do_export(self, arg):
        """Usage: export   (<filename>)"""

        export(arg)

    @parser
    def do_import(self, arg):
        """Usage: import   (<filename>)"""

        importnotes(arg)

    @parser
    def do_next(self, arg):
        """Usage: next  """
        nextquery(arg)

    def do_quit(self, arg):
        """Exit application."""

        print('See you later!')
        exit()

opt = docopt(__doc__, sys.argv[1:])

"""Creates a newnote,saving it
"""


def createnewnote(docopt_args):
    notebody = ""
    if docopt_args["<note_title>"] and docopt_args["-m"]:
        with indent(4, quote=' >'):
            # puts(
            #     colored.yellow('Type the body of the notes.Press "/pq" to save & exit'))
            print(Back.YELLOW + Fore.RED + 'Type the body of the notes' + Back.RESET + Fore.RESET + Style.BRIGHT + ' (Press ' + Back.YELLOW + Fore.RED + "/pq" + Back.RESET + Fore.RESET + ' to save & exit)' + Style.NORMAL + Fore.GREEN)
        sentinel = '/pq'  # ends when this string is seen
        for line in iter(raw_input, sentinel):
            notebody += line + "\n"
    print(Fore.RESET)
    notetitle = docopt_args["<note_title>"]
    note = NoteOperations()
    note.save(title=notetitle, body=notebody)
    with indent(4, quote='√ '):
        puts(colored.green("Successfully saved"))
    note.synctocloud()

"""View a single note by id
"""


def viewsinglenote(docopt_args):
    noteid = docopt_args["<note_id>"]
    if docopt_args["-m"]:
        note = NoteOperations()
        contents = note.view(noteid)

    else:
        note = NoteOperations()
        contents = note.view(noteid)
        with indent(4, quote=' >'):
            puts(
                colored.green(contents.get("title", "========NOT FOUND=======")))
        with indent(4):
            puts(
                colored.yellow(contents.get("body", "========NOT FOUND=======")))

"""Deletes a single note by id or all
"""


def deletenote(docopt_args):
    noteid = docopt_args["<note_id>"]
    note = NoteOperations()

    if docopt_args["-a"]:
        puts(
            "Are you sure you want to delete all notes? [" + colored.red("y") + "][" + colored.green("n") + "]")
        answer = raw_input(">")
        if answer == "y":
            status = note.delete(noteid, "all")
        else:
            return
    else:
        puts("Are you sure you want to delete note " + str(note.getnotetitle(noteid)
                                                           ) + "? [" + colored.red("y") + "][" + colored.green("n") + "]")
        answer = raw_input(">")
        if answer == "y":
            notetitle = note.getnotetitle(noteid)
            status = note.delete(noteid, "one")
        else:
            return

    if status > 0:
        with indent(4, quote=' √'):
            if docopt_args["-a"]:
                puts(colored.red("Successfully deleted all notes"))
                note = NoteOperations()
                note.deletenotesfromcloud()
            else:
                puts(colored.red("Successfully deleted note ") +
                     colored.yellow(notetitle))
                note = NoteOperations()
                note.synctocloud()
    else:
        with indent(4, quote=' √'):
            puts(colored.red("Sorry,the note with id ") +
                 colored.green(noteid) + colored.red(" does not exist"))

"""Lists all notes or for a certain limit
"""


def listnotes(docopt_args):
    if docopt_args["--limit"]:
        limit = docopt_args["<items>"]
        insertvaluecache("list", str(limit), "")
        # Scrible().hasnext = "list" + str(limit)
        # print "next" + Scrible().hasnext
        note = NoteOperations()
        allnotes = note.viewall(limit)
    else:
        note = NoteOperations()
        allnotes = note.viewall()
    if len(allnotes) > 0:
        for item in allnotes:
            with indent(4, quote=' >'):
                noteid = item.get("_id", "")
                time = "["+ item.get("datecreated", "") + "]"
                noteids = "["+ str(noteid) + "]"
                body = item.get("body", "")
                title = item.get("title", "========NOT FOUND=======")
                print(Fore.YELLOW + "===============================================" + Fore.RESET)
                print(Back.BLUE + noteids + Back.RESET +"  " + Back.BLUE + time  + Back.RESET +"\n\n" + Back.RED + title +  Back.RESET + Style.BRIGHT +"\n\n"+ Fore.GREEN + body + Fore.RESET + Style.NORMAL)
                print(Fore.YELLOW + "===============================================" + Fore.RESET)
    else:
        with indent(4):
            puts(colored.yellow("Sorry, no notes present"))

"""Searches all notes or for a certain limit
"""


def searchnotes(docopt_args):
    query = docopt_args["<query_string>"]
    if docopt_args["--limit"]:
        limit = docopt_args["<items>"]
        insertvaluecache("search", str(limit), query)
        note = NoteOperations()
        notes = note.search(query, limit)
    else:
        note = NoteOperations()
        notes = note.search(query)
    if len(notes) > 0:
        for item in notes:
            noteid = item.get("_id", "")
            time = "["+ item.get("datecreated", "") + "]"
            noteids = "["+ str(noteid) + "]"
            body = item.get("body", "")
            title = item.get("title", "========NOT FOUND=======")
            print(Fore.YELLOW + "===============================================" + Fore.RESET)
            print(Back.BLUE + noteids + Back.RESET +"  " + Back.BLUE + time  + Back.RESET +"\n\n" + Back.RED + title +  Back.RESET + Style.BRIGHT +"\n\n"+ Fore.GREEN + body + Fore.RESET + Style.NORMAL)
            print(Fore.YELLOW + "===============================================" + Fore.RESET)
    else:
        puts(colored.red("Sorry,the query does not match any notes"))

"""Sync notes with cloud
"""


def synctocloud(docopt_args):
    note = NoteOperations()
    note.synctocloud()

"""Imports notes from csv file
"""


def importnotes(docopt_args):
    filename = docopt_args["<filename>"] + ".csv"
    if os.path.isfile(filename):
        with open(filename, 'rb') as f:
            reader = csv.reader(f)
            for row in reader:
                title = row[0]
                body = row[1]
                time = row[2]
                note = NoteOperations()
                note.save(title=title, body=body)
            with indent(4, quote=' >'):
                puts(colored.green("Import successful"))
            note.synctocloud()
    else:
        with indent(4, quote=' >'):
            puts(colored.red("Sorry,the file does not exist"))

"""Exports notes to a csv file
"""


def export(docopt_args):
    filename = docopt_args["<filename>"]
    finalfilepath = filename + ".csv"
    note = NoteOperations()
    allnotes = note.viewall()
    if len(allnotes) > 0:
        noteslist = []
        for item in allnotes:
            title = item.get("title", "")
            body = item.get("body", "")
            timedate = item.get("datecreated", "")
            templist = [title, body, timedate]
            noteslist.append(templist)
        with open(finalfilepath, 'wb') as fp:
            a = csv.writer(fp, delimiter=',')
            a.writerows(noteslist)
            puts(colored.green(
                "Notes exported successfully to " + os.getcwd() + "/" + finalfilepath))
    else:
        with indent(4):
            puts(colored.yellow("Sorry, no notes present"))

"""Returns next set of note items when lilit was specified
"""


def nextquery(docopt_args):
    values = readvaluescache()
    if len(values) > 0:
        op = values.get("op", "")
        if op == "list":
            skip = values.get("skip", "")
            note = NoteOperations()
            allnotes = note.viewallskip(str(skip), str(skip))
            if len(allnotes) > 0:
                insertvaluecache("list", str(int(skip) + int(skip)), "")
                for item in allnotes:
                    noteid = item.get("_id", "")
                    time = "["+ item.get("datecreated", "") + "]"
                    noteids = "["+ str(noteid) + "]"
                    body = item.get("body", "")
                    title = item.get("title", "========NOT FOUND=======")
                    print(Fore.YELLOW + "===============================================" + Fore.RESET)
                    print(Back.BLUE + noteids + Back.RESET +"  " + Back.BLUE + time  + Back.RESET +"\n\n" + Back.RED + title +  Back.RESET + Style.BRIGHT +"\n\n"+ Fore.GREEN + body + Fore.RESET + Style.NORMAL)
                    print(Fore.YELLOW + "===============================================" + Fore.RESET)
            else:
                with indent(4):
                    puts(colored.yellow("End of notes"))
        elif op == "search":
            skip = values.get("skip", "")
            query = values.get("query", "")
            note = NoteOperations()
            allnotes = note.searchskip(query, str(skip), str(skip))
            if len(allnotes) > 0:
                insertvaluecache("search", str(int(skip) + int(skip)), query)
                for item in allnotes:
                    noteid = item.get("_id", "")
                    time = "["+ item.get("datecreated", "") + "]"
                    noteids = "["+ str(noteid) + "]"
                    body = item.get("body", "")
                    title = item.get("title", "========NOT FOUND=======")
                    print(Fore.YELLOW + "===============================================" + Fore.RESET)
                    print(Back.BLUE + noteids + Back.RESET +"  " + Back.BLUE + time  + Back.RESET +"\n\n" + Back.RED + title +  Back.RESET + Style.BRIGHT +"\n\n"+ Fore.GREEN + body + Fore.RESET + Style.NORMAL)
                    print(Fore.YELLOW + "===============================================" + Fore.RESET)
            else:
                with indent(4):
                    puts(colored.yellow("End of notes"))
    else:
        pass

"""Create Cache for holding last limit and operation
"""


def createcache():
    with open("cache", 'wb') as fp:
        a = csv.writer(fp, delimiter=',')
        noteslist = ""
        a.writerows(noteslist)

"""Inserts into cache last limit and operation
"""


def insertvaluecache(op, sk, query):
    with open("cache", 'wb') as fp:
        a = csv.writer(fp, delimiter=',')
        noteslist = [[op, sk, query]]
        a.writerows(noteslist)

"""Reads cache to get last operation and limit
"""


def readvaluescache():
    file = open("cache")
    numline = len(file.readlines())
    if numline > 0:
        with open("cache", 'rb') as f:
            reader = csv.reader(f)
            for row in reader:
                op = row[0]
                skip = row[1]
                query = row[2]
            return {'op': op, 'skip': skip, 'query': query}
    else:
        return {}
"""show nice welcome message
"""


def showwelcomemsg():
    init(strip=not sys.stdout.isatty())  # strip colors if stdout is redirected
    cprint(figlet_format('Scrible', font='starwars'),
           'green', attrs=['blink'])
    print(Back.RED + 'Welcome to Scrible NoteApp!' + Back.RESET + Style.DIM + '\n(type help for a list of commands.)' + Style.NORMAL)


"""starts application when -start is specified
"""

if opt['--start']:
    createcache()
    showwelcomemsg()
    Scrible().cmdloop()  # creates the REPL

print(opt)
