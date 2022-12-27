"""
Run function to call to the Syncer class and to make report.
"""
from .syncer import Syncer
import argparse


def synchronize(sourcedir, targetdir, interval, log_file_path):
    """Calls to Syncer class, makes comparison, copies content and outputs logs.

    :param sourcedir: the source folder location
    :param targetdir: the replica folder location. Will be created if doesn't exist.
    :param interval: synchronization interval
    :param log_file_path: the log file location. Will be created if doesn't exist.
    """
    syncer = Syncer(sourcedir, targetdir, interval, log_file_path)
    syncer.sync_work()
    syncer.print_logs()


def args_parser():
    """Parser of input arguments. Returns all input arguments from command line."""
    parser = argparse.ArgumentParser(
        description='''This is a Python package that synchronizes two folders: source and replica. The
    program maintains a full, identical copy of source folder at replica folder.''')
    parser.add_argument('sourcedir', help='Location of the source folder.')
    parser.add_argument('targetdir',
                        help='Location of the replica folder. If the folder doesn\'t exist at this directory, '
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
    return args
