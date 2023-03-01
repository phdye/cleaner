# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------

import os

# ------------------------------------------------------------------------------


class ChDir (object):

    """
    Context manager to step into a directory temporarily.
      - On entry, caches original working directory
      - Changes to the user specified working directory
      - On exit, changes back to original working directory

      with Chdir('working/area') :
          do some work

    Lifted whole from :
       https://pythonadventures.wordpress.com/2013/12/15/chdir-a-context-manager-for-switching-working-directories/
    """

    __slots__ = ('old_dir', 'new_dir')

    def __init__(self, path):
        self.old_dir = os.getcwd()
        self.new_dir = path

    def __enter__(self):
        os.chdir(self.new_dir)

    def __exit__(self, *args):
        os.chdir(self.old_dir)

# ------------------------------------------------------------------------------
