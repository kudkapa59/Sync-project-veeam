from dirsync_1 import sync
from dirsync_1 import interval_work
# from sync import sync
# from dirsync import sync
import logging
import os
import sys

# interval = 10
# sync('folder_1', 'folder_2', 'sync', interval,  'C:/Users/Kapa/Desktop/log.txt', purge=True)
# data = os.fsencode(sys.argv[1])
sourcedir = os.fsencode(sys.argv[1])
targetdir = os.fsencode(sys.argv[2])
interval = os.fsencode(sys.argv[3])
log_file_path = os.fsencode(sys.argv[4])
# print(data)
interval_work(sourcedir.decode('utf-8'), targetdir.decode('utf-8'), interval, log_file_path.decode('utf-8'))
