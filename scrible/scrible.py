#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Scrible

    Usage: 
        Scrible.py createnote  (<note_title>) [-m]
        Scrible.py viewnote    (<note_id>)
        Scrible.py deletenote  (<note_id>)
        Scrible.py searchnotes (<query_string>) [--limit]
        Scrible.py viewnote    (<note_id>)
        Scrible.py listnotes   [--limit]

    Options:
        -h,--help       : show this help message
        createnote     : creates a note with a certain message
        viewnote       : view a single note using id
        deletenote     : deletes a single note
        limit          : Limit of notes to list
        searchnotes (<query_string>) [--limit]: View a formatted list of all/
                        specific number of the notes identified by query string
        listnotes [--limit] :View specific number of notes
        next           :See next set of data in current query
"""

from docopt import docopt
from notes.noteoperations import NoteOperations
from clint.textui import colored, puts, indent



def main(docopt_args):
    """ main-entry point for program, expects dict with arguments from docopt()
    """

    # User passed the required argument
    if docopt_args["createnote"]:  # user wants to create a new note
        if docopt_args["<note_title>"] and docopt_args["-m"]:
            notetitle = docopt_args["<note_title>"]
            notebody = ""
            with indent(4, quote=' >'):
                puts(colored.red('Type the body of the notes.Press "/pq" when finished.'))
            sentinel = '/pq' # ends when this string is seen
            for line in iter(raw_input, sentinel):
                notebody += line + "\n"

        notetitle = docopt_args["<note_title>"]
        note = NoteOperations()
        note.save(title = notetitle,body = notebody)





# START OF SCRIPT
if __name__ == "__main__":
    args = docopt(__doc__)
    main(args)
