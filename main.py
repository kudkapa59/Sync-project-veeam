
# from dirsync import sync
from sync import sync
import logging
import sys

interval = 3000
# sync('folder_1', 'folder_2', 'sync', purge=True)
sync('folder_1', 'folder_2', interval, 'log.txt')