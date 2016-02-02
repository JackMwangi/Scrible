#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" docopt_example.py
    
    Usage:
        docopt_example.py -h
        docopt_example.py <ggghh> [-f | -g | -o ]
        docopt_example.py <repeating>...
    Options:
        -h,--help       : show this help message
        required        : example of a required argument
        repeating       : example of repeating arguments
        -f,--flag       : example flag #1
        -g,--greatflag  : example of flag #2
        -o,--otherflag  : example of flag #3
"""
# the above is our usage string that docopt will read and use to determine
# whether or not the user has passed valid arguments.
# import the docopt function from the docopt module
from docopt import docopt
def main(docopt_args):
    """ main-entry point for program, expects dict with arguments from docopt() """
    
    # Notice, no checking for -h, or --help is written here.
    # docopt will automagically check for it and use your usage string.
    
    # User passed the required argument
    if docopt_args["<ggghh>"]:
        print "You have used the required argument: " + docopt_args["<ggghh>"]
        
        # Get flags used
        if docopt_args["--flag"]:
            print "   with --flag\n"
        elif docopt_args["--greatflag"]:
            print "   with --greatflag\n"
        elif docopt_args["--otherflag"]:
            print "   with --otherflag\n"
        else:
            print "   with no flags.\n"
    # User passed 1 or more repeating arguments
    elif docopt_args["<repeating>"]:
        print "You have used the repeating args:"
        print '   ' + '\n   '.join(docopt_args["<repeating>"]) + '\n'
# START OF SCRIPT
if __name__ == "__main__":
    # Docopt will check all arguments, and exit with the Usage string if they
    # don't pass.
    # If you simply want to pass your own modules documentation then use __doc__,
    # otherwise, you would pass another docopt-friendly usage string here.
    # You could also pass your own arguments instead of sys.argv with: docopt(__doc__, argv=[your, args])
    args = docopt(__doc__)
    # We have valid args, so run the program.
    main(args)