import sys

from pathlib import Path

import unittest

from plumbum import local, FG, BG, RETCODE

from chdir import ChDir
from ansi import ansi_escape

import cygport

#------------------------------------------------------------------------------

examples = Path('tests', 'examples')

class Test_Case ( unittest.TestCase ) :

    def test_missing_cygport_file ( self ) :

        with ChDir(examples / 'none') :
            ( retcode, stdout, stderr ) = local[sys.executable]['-m','cygport', '.', 'prep'].run(retcode=None)

        stdout = ansi_escape.sub('', stdout)
        stderr = ansi_escape.sub('', stderr)

        self.assertEqual ( retcode, 1 )
        self.assertEqual ( stdout, '' )

        self.assertEqual ( stderr, "cygport:  No .cyport file found.  For usage 'cygport --help'\n")

    def test_single_cygport_file ( self ) :

        with ChDir(examples / 'single') :
            ( retcode, stdout, stderr ) = local[sys.executable]['-m','cygport', '.', 'prep'].run(retcode=None)

        stdout = ansi_escape.sub('', stdout)
        stderr = ansi_escape.sub('', stderr)

        # with open('stdout.raw', 'w') as f:
        #     f.write(stdout)
        # with open('stderr.raw', 'w') as f:
        #     f.write(stderr)

        self.assertEqual ( retcode, 1 )
        self.assertEqual ( stdout, '' )

        self.assertEqual ( stderr, "*** ERROR: SRC_URI must be defined\n")

    def test_multiple_cygport_files ( self ) :

        with ChDir(examples / 'multiple') :
            ( retcode, stdout, stderr ) = local[sys.executable]['-m','cygport', '.', 'prep'].run(retcode=None)

        stdout = ansi_escape.sub('', stdout)
        stderr = ansi_escape.sub('', stderr)

        self.assertEqual ( retcode, 1 )
        self.assertEqual ( stdout, '' )

        self.assertEqual ( stderr, "cygport:  More than one .cyport file found.  For usage 'cygport --help'\n")


#------------------------------------------------------------------------------
