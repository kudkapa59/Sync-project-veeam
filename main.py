"""
Takes all input arguments. Schedules the synchronization with the input interval.
"""

from sync import synchronize
import schedule
import argparse

parser = argparse.ArgumentParser(
    description='''This is a Python package that synchronizes two folders: source and replica. The
program maintains a full, identical copy of source folder at replica folder.''')
parser.add_argument('sourcedir', help='Location of the source folder.')
parser.add_argument('targetdir', help='Location of the replica folder. If the folder doesn\'t exist at this directory, '
                                      'it will be created.')
parser.add_argument('interval', type=float,
                    help='Synchronization interval. Stays for with what frequency synchronization'
                         'should be repeated. Float argument.')
parser.add_argument('--time_units', choices=['s', 'm', 'h'],
                    help='Time measurement units. Possible values: s for seconds, m for minutes,'
                         'h for hours. Default value is seconds', default='s')
parser.add_argument('log_file_path', help='Log file path. If the file doesn\'t exist, '
                                          'it will be created.')
args = parser.parse_args()


if __name__ == '__main__':
    synchronize(args.sourcedir, args.targetdir, str(args.interval) + args.time_units, args.log_file_path)

    if args.time_units == 's':
        schedule.every(args.interval).seconds.do(synchronize, args.sourcedir,
                                                 args.targetdir, str(args.interval) + args.time_units,
                                                 args.log_file_path)
    elif args.time_units == 'm':
        schedule.every(args.interval).minutes.do(synchronize, args.sourcedir,
                                                 args.targetdir, str(args.interval) + args.time_units,
                                                 args.log_file_path)
    else:
        schedule.every(args.interval).hours.do(synchronize, args.sourcedir,
                                               args.targetdir, str(args.interval) + args.time_units, args.log_file_path)

    while 1:
        schedule.run_pending()