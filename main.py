from sync import sync
import logging
import os
import sys
import schedule
import time

import argparse

parser = argparse.ArgumentParser(
    description='''This is a Python package that synchronizes two folders: source and replica. The
program maintains a full, identical copy of source folder at replica folder.''',
    epilog="""All is well that ends well.""")
# parser.add_argument('--foo', type=int, default=42, help='FOO!')
parser.add_argument('sourcedir', nargs='*', help='Location of the source folder.')
parser.add_argument('targetdir', nargs='*', help='Location of the replica folder. If the folder doesn\'t exist at this directory, '
                                                 'it will be created.')
parser.add_argument('interval', type=float, nargs='*', help='Synchronization interval. Stays for with what frequency synchronization'
                                                'should be repeated. Float argument.')
parser.add_argument('time_units', nargs='*', help='Time measurement units. Possible values: s for seconds, m for minutes,'
                                                    'h for hours')
parser.add_argument('log_file_path', nargs='*', help='Log file path. If the file doesn\'t exist, '
                                                       'it will be created.')
args=parser.parse_args()

# parser.add_argument('--name', type=str, required=True)
# # Parse the argument
# args = parser.parse_args()
# # Print "Hello" + the user input argument
# print('Hello,', args.name)

sourcedir = sys.argv[1]
targetdir = sys.argv[2]
interval = float(sys.argv[3])
time_units = sys.argv[4]
log_file_path = sys.argv[5]

sync(sourcedir, targetdir, str(interval) + time_units,  log_file_path)

if time_units == 's':
    schedule.every(interval).seconds.do(sync, sourcedir,
                                        targetdir, str(interval) + time_units, log_file_path)
elif time_units == 'm':
    schedule.every(interval).minutes.do(sync, sourcedir,
                                        targetdir, str(interval) + time_units, log_file_path)
elif time_units == 'h':
    schedule.every(interval).hours.do(sync, sourcedir,
                                        targetdir, str(interval) + time_units, log_file_path)
else:
    raise ValueError("Not suitable time units")

while 1:
    schedule.run_pending()

