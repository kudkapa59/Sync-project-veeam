"""
dirsync's functions
"""

from __future__ import print_function
from apscheduler.schedulers.background import BackgroundScheduler

import sys
import os
import time

import threading
from .syncer import Syncer
sched = BackgroundScheduler()

def interval_work(sourcedir, targetdir, interval, log_file_path):
    # threading.Timer(interval, lambda: sync(sourcedir, targetdir, action, interval, log_file_path, **options)).start()
    # sched.add_job(lambda: sync(sourcedir, targetdir, action, interval, log_file_path, **options), 'interval', seconds=interval)
    # sched.start()

    # sched.shutdown()
    sync(sourcedir, targetdir, interval, log_file_path)
    # return 1

def sync(sourcedir, targetdir, interval, log_file_path):
    copier = Syncer(sourcedir, targetdir, interval, log_file_path)
    copier.do_work()

    # print report at the end
    copier.report()

    return set(copier._changed).union(copier._added).union(copier._deleted)


def from_cmdline():
    from .options import ArgParser, USER_CFG_FILE, DEFAULT_USER_CFG

    # create config file if it does not exist
    user_cfg_file = os.path.expanduser(USER_CFG_FILE)
    if not os.path.isfile(user_cfg_file):
        print('Creating user config file "%s" ...' % user_cfg_file, end=''),
        with open(user_cfg_file, 'w') as f:
            f.write(DEFAULT_USER_CFG)
        print(' Done')

    try:
        sync(**vars(ArgParser().parse_args()))
    except Exception as e:
        sys.stdout.write(str(e) + '\n')
        sys.exit(2)
