#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys

from pathlib import Path

from plumbum.cmd import invoke

#------------------------------------------------------------------------------

TEST_INFO_OPTION = '--test:info'

test_info = TEST_INFO_OPTION in sys.argv
if test_info :
    sys.argv.remove(TEST_INFO_OPTION)

def eprint(x):
    if test_info:
        print(x, file=sys.stderr)

#------------------------------------------------------------------------------

# Must be executed from top of package.
eprint('# ')
# eprint("# Prepending module search with with [ 'build/lib', '.' ]")
eprint("# Prepending module search with with [ '.' ]")
sys.path.insert(0, '.')
# sys.path.insert(0, 'build/lib') # favor build/lib
eprint('#')

#------------------------------------------------------------------------------

from cleaner import __file__ as _modpath
if _modpath.endswith("__init__.py") :
    module_path = Path(_modpath).parent
else:
    module_path = _modpath
eprint(f"# Imported:  '{module_path}'  [From the source tree if relative]\n#")

#------------------------------------------------------------------------------

if __name__ == '__main__':
    from cleaner import main
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    argstring = "'" + ( "' '".join(sys.argv) ) + "'"
    eprint(f"# Calling main ( {argstring} )\n#")
    sys.exit(main(sys.argv))

#------------------------------------------------------------------------------
