"""
"""

from __future__ import print_function
from .syncer import Syncer


def sync(sourcedir, targetdir, interval, log_file_path):
    copier = Syncer(sourcedir, targetdir, interval, log_file_path)
    copier.do_work()
    copier.report()
