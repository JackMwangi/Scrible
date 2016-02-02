#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Scrible.py
    Usage:
        Scrible.py -h
        Scrible.py <required> [-f | -g | -o ]
        Scrible.py <repeating>...
    Options:
        -h,--help       : show this help message
        -g,--save  : example of flag #2
"""

from docopt import docopt


def main(docopt_args):  
    """ main-entry point for program, expects dict with arguments from docopt() 
    """

    # User passed the required argument
    if docopt_args["<required>"]:
        # You have used the required argument: " + docopt_args["<required>"]
        if docopt_args["--save"]:
            print "   with --flag\n"

    else:
        print "without required"


# START OF SCRIPT
if __name__ == "__main__":
    args = docopt(__doc__)
    main(args)
