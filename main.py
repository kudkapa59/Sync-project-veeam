"""
Takes all input arguments. Schedules the synchronization with the input interval.

This is a Python package that synchronizes two folders: source and replica. The
program maintains a full, identical copy of source folder at replica folder.

To implement it you should be in the folder 'veeam_task' and write into console command
"python main.py "sourcedir" "targetdir" interval "log_file_path" ".

positional arguments:
    :param sourcedir: Location of the source folder.
    :param targetdir: Location of the replica folder. If the folder doesn't exist at this directory, it will be created.
    :param interval: Synchronization interval. Stays for with what frequency synchronization should be repeated. Float argument.
    :param log_file_path: Log file path. If the file doesn't exist, it will be created.

optional arguments:
    :param -h, --help: Show this help message and exit.
    :param time_units {s,m,h}: Time measurement units. Possible values: s for seconds, m for minutes,h for hours. Default value is seconds.

"""

from sync import synchronize, args_parser
import schedule

if __name__ == '__main__':
    args = args_parser()

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
