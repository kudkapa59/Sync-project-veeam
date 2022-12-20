from sync import sync
import logging
import os
import sys
import schedule
import time

sourcedir = sys.argv[1]
targetdir = sys.argv[2]
interval = int(sys.argv[3])
log_file_path = sys.argv[4]

sync(sourcedir, targetdir, log_file_path)
# schedule.every(interval).minutes.do(interval_work, sourcedir.decode('utf-8'),
#                                     targetdir.decode('utf-8'), log_file_path.decode('utf-8'))
schedule.every(interval).seconds.do(sync, sourcedir,
                                    targetdir, log_file_path)

while 1:
    schedule.run_pending()

