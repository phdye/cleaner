#!/usr/bin/env python3
#------------------------------------------------------------------------------

"""
cleaner — automatically remove unwanted files

Usage: cleaner [options] [-v...] [ <directory> ...]

The cleaner utility searches through the filesystem for "temporary files"
which can be deleted safely.

Options :
  --debug        Show internal handling such as parsed arguments.
  -v, --verbose  Show additional processing info.
  -h, --help     Show this usage message.
  --version      Show version and exit.

Python implementation of Chris Newel's niftyclean (late 80's at CMUCS).
Or, per the source clean-1.4, perhaps originally written by Jay Leafer.

Report any issues at https://github.com/phdye/cleaner/issues.
"""

from __future__ import print_function

import sys
import os
import re
import fnmatch

from glob import glob

from pathlib import Path

from docopt import docopt

from cleaner import __version__

from .fields import fields

#------------------------------------------------------------------------------

def main ( argv = sys.argv ) :

    cfg = fields(docopt(__doc__, argv=argv[1:], options_first=True, version=__version__ ))

    junk = load_patterns(cfg, "~/.cleanrc")

    if cfg.opt.verbose :
        print(f"Scanning ...")

    candidates = []
    for root, dirs, files in os.walk('.') :
        if cfg.opt.verbose :
            print(f"- {root}")
        root = Path(root)
        for file_name in files :
            if junk.match(file_name) :
               candidates.append ( str( root / file_name ) )

    if cfg.opt.verbose :
        print('')
        if len(candidates) <= 0:
            print("No junk files found :)\n")

    if len(candidates) > 0 :
        print("Junk files found :\n  " + "\n  ".join(candidates))
        response = input("\nDelete these files [y/N] ? ")
        # action = 'delete junk files' if response.lower() in [ 'y', 'yes' ] else 'do nothing'
        # print(f"=> '{response}'  =>  {action}")
        if response.lower() in [ 'y', 'yes' ] :
            for file_path in candidates :
                if cfg.opt.verbose >= 7:
                    print(f"- removing '{file_path}'")
                os.remove(file_path)

    return 0

#------------------------------------------------------------------------------

def load_patterns(cfg, file):
    file = os.path.expanduser(file)
    if cfg.opt.verbose:
        print(f"Loading patterns from '{file}'")
    with open(file, 'r') as f:
        lines = f.readlines()

    lines = [ s.strip() for s in lines ]
    lines = [ s for s in lines if len(s) > 0 ]
    lines = [ s for s in lines if not s[0] == '#' ]

    # print("patterns:\n" + '\n'.join(lines) + "\n- - -")

    # lines = [ '*~', '*.BAK' ]

    patterns = [ fnmatch.translate(s) for s in lines ]

    if cfg.opt.verbose >= 3:
        print("Glob pattern to regex translation :")
        for idx in range(len(patterns)):
            glob = f"'{lines[idx]}'"
            regex = f"'{patterns[idx]}'"
            print(f" {glob:<20} => {regex}")

    expression = '^(' + '|'.join(patterns) + ')$'

    if cfg.opt.verbose >= 5:
        print(f"Complete regular expression :\n{expression}\n")
        
    return re.compile(expression)

#------------------------------------------------------------------------------

if __name__ == "__main__":
    sys.exit(main(sys.argv))

#------------------------------------------------------------------------------
