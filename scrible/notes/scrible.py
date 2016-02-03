#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This shows the usage and options that available for the Scrible note taking app
Usage:
    scrible createnote  (<note_title>) [-m]
    scrible viewnote    (<note_id>)
    scrible deletenote  (<note_id>)
    scrible searchnotes (<query_string>) [(--limit=<items>)]
    scrible viewnote    (<note_id>)
    scrible listnotes   [(--limit=<items>)]
    scrible next
    scrible (-s | --start)
    scrible (-h | --help | --version)
Options:
    -s, --start  Interactive Mode
    -h, --help  Show this screen and exit.
    -m          Starts creating note body
"""

import sys
import cmd
from docopt import docopt, DocoptExit
from noteoperations import NoteOperations
from clint.textui import colored, puts, indent



def docopt_cmd(func):
    """
    Used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """
    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print('Invalid Command!')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn



class Scrible (cmd.Cmd):
    intro = 'Welcome to scrible NoteApp!' \
        + ' (type help for a list of commands.)'
    prompt = '(Scrible) '
    file = None

    @docopt_cmd
    def do_createnote(self, arg):
        """Usage: createnote  (<note_title>) [-m]"""

        createnewnote(arg)

    @docopt_cmd
    def do_viewnote(self, arg):
        """Usage: viewnote    (<note_id>)"""

        viewsinglenote(arg)

    @docopt_cmd
    def do_deletenote(self, arg):
        """Usage: deletenote  (<note_id>)"""

        deletenote(arg)

    @docopt_cmd
    def do_searchnotes(self, arg):
        """Usage: searchnotes (<query_string>) [(--limit=<items>)]"""

        searchnotes(arg)

    @docopt_cmd
    def do_listnotes(self, arg):
        """Usage: listnotes   [(--limit=<items>)]"""

        listnotes(arg)

    def do_quit(self, arg):
        """Quits out of Interactive Mode."""

        print('Good Bye!')
        exit()

opt = docopt(__doc__, sys.argv[1:])


def createnewnote(docopt_args):
    notebody = ""
    if docopt_args["<note_title>"] and docopt_args["-m"]:
        with indent(4, quote=' >'):
            puts(colored.red('Type the body of the notes.Press "/pq" when finished.'))
        sentinel = '/pq' # ends when this string is seen
        for line in iter(raw_input, sentinel):
            notebody += line + "\n"

    notetitle = docopt_args["<note_title>"]
    note = NoteOperations()
    note.save(title = notetitle,body = notebody)

def viewsinglenote(docopt_args):
    noteid = docopt_args["<note_id>"]
    note = NoteOperations()
    contents = note.view(noteid)
    with indent(4, quote=' >'):
        puts(colored.green(contents.get("title","========NOT FOUND=======")))
    with indent(4):
        puts(colored.yellow(contents.get("body","========NOT FOUND=======")))

def deletenote(docopt_args):
    noteid = docopt_args["<note_id>"]
    note = NoteOperations()
    notetitle = note.getnotetitle(noteid)
    status = note.delete(noteid)
    if status > 0 :
        with indent(4, quote=' >'):
            puts(colored.red("Successfully deleted note ") + colored.green(notetitle))
    else :
        with indent(4, quote=' >'):
            puts(colored.red("Sorry,the note with id ") + colored.green(noteid) + colored.red(" does not exist"))

def listnotes(docopt_args):
    if docopt_args["--limit"]:
        limit = docopt_args["<items>"]
        note = NoteOperations()
        allnotes = note.viewall(limit)
    else:
        note = NoteOperations()
        allnotes = note.viewall()
    for item in allnotes:
        with indent(4, quote=' >'):
            puts(colored.green(item.get("title","========NOT FOUND=======")))
        with indent(4):
            puts(colored.yellow(item.get("body","========NOT FOUND=======")))

def searchnotes(docopt_args):
    query = docopt_args["<query_string>"]
    if docopt_args["--limit"]:
        limit = docopt_args["<items>"]
        note = NoteOperations()
        notes = note.search(query, limit)
    else:
        note = NoteOperations()
        notes = note.search(query)
    for item in notes:
        with indent(4, quote=' >'):
            puts(colored.green(item.get("title","---------------")))
        with indent(4):
            puts(colored.yellow(item.get("body","---------------")))

def next(docopt_args):
    pass



if opt['--start']:
    Scrible().cmdloop()

print(opt) 