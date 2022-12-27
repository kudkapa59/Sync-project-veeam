"""
Takes all input arguments. Schedules the synchronization with the input interval.
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
