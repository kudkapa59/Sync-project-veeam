"""
Run function to call to the Syncer class and to make report.
"""
from .syncer import Syncer


def synchronize(sourcedir, targetdir, interval, log_file_path):
    """Calls to Syncer class, makes comparison, copies content and outputs logs."""
    syncer = Syncer(sourcedir, targetdir, interval, log_file_path)
    syncer.sync_work()
    syncer.print_logs()
