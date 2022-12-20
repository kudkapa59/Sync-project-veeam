from sync import sync
from sync import interval_work
# from sync import sync
# from dirsync import sync
import logging
import os
import sys

# sync('folder_1', 'folder_2', 'sync', purge=True)
sourcedir = os.fsencode(sys.argv[1])
targetdir = os.fsencode(sys.argv[2])
interval = os.fsencode(sys.argv[3])
log_file_path = os.fsencode(sys.argv[4])
interval_work(sourcedir.decode('utf-8'), targetdir.decode('utf-8'), interval, log_file_path.decode('utf-8'))
