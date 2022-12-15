
from dirsync import sync
import logging
import sys


sync('folder_1', 'folder_2', 'sync', purge=True)