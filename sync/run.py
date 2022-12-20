"""
"""
from .syncer import Syncer


def sync(sourcedir, targetdir, interval, log_file_path):
    """Calls to Syncer class, makes comparison, copies content and outputs logs."""
    copier = Syncer(sourcedir, targetdir, interval, log_file_path)
    copier.do_work()
    copier.report()
