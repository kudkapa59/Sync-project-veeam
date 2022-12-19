from dirsync_1 import sync
from dirsync_1 import interval_work
# from sync import sync
# from dirsync import sync
import logging
import sys

interval = 10
# sync('folder_1', 'folder_2', 'sync', interval,  'C:/Users/Kapa/Desktop/log.txt', purge=True)
interval_work('folder_1', 'folder_3', interval, 'C:/Users/Kapa/Desktop/log.txt')

# sync('folder_1', 'folder_2', interval, 'log.txt')