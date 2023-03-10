"""
"""

import os
import sys
import stat
import time
import shutil
import logging
import filecmp

__pkg_name__ = 'sync'


class DCMP(object):
    """Class to store unique values in source and replica folders, and common files in these folders"""

    def __init__(self, l, r, c):
        self.left_only = l
        self.right_only = r
        self.common = c


class Syncer(object):
    """Modifies the replica folder to exactly match content of the source folder.

    :param sourcedir: the source folder location
    :param targetdir: the replica folder location. Will be created if doesn't exist.
    :param interval: synchronization interval
    :param log_file_path: the log file location. Will be created if doesn't exist.
    """

    def __init__(self, dir1, dir2, interval, log_file_path):
        self._log_file_path = log_file_path

        # logging configuration to print logs to console and to the specified file
        log = logging.getLogger('sync')
        log.setLevel(logging.INFO)
        if not log.handlers:
            hdl = logging.StreamHandler(sys.stdout)
            hdl.setFormatter(logging.Formatter('%(message)s'))
            log.addHandler(hdl)
        self.logger = log
        logging.basicConfig(filename=self._log_file_path,
                            filemode='a',
                            format='%(asctime)s %(name)s %(levelname)s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            level=logging.DEBUG)
        self.log('Synchronization interval: %s' % interval)

        self._dir1 = dir1
        self._dir2 = dir2

        self._changed = []
        self._added = []
        self._deleted = []

        # stat vars
        self._numdirs = 0
        self._numfiles = 0
        self._numdelfiles = 0
        self._numdeldirs = 0
        self._numnewdirs = 0
        self._numcontupdates = 0
        self._numtimeupdates = 0
        self._starttime = 0.0
        self._endtime = 0.0

        # failure stat vars
        self._numcopyfld = 0
        self._numupdsfld = 0
        self._numdirsfld = 0
        self._numdelffld = 0
        self._numdeldfld = 0

        if not os.path.isdir(self._dir1):
            raise ValueError("Error: Source directory does not exist.")

    def log(self, msg=''):
        """Reference to the logger.
        """
        self.logger.info(msg)

    def _compare(self, dir1, dir2):
        """Compares source and replica folders.

        :param dir1: the source folder location.
        :param dir2: the replica folder location.
        """

        left = set()
        right = set()

        self._numdirs += 1

        for cwd, dirs, files in os.walk(dir1):
            self._numdirs += len(dirs)
            for f in dirs + files:
                path = os.path.relpath(os.path.join(cwd, f), dir1)
                re_path = path.replace('\\', '/')

                left.add(path)
                anc_dirs = re_path[:-1].split('/')
                anc_dirs_path = ''
                for ad in anc_dirs[1:]:
                    anc_dirs_path = os.path.join(anc_dirs_path, ad)
                    left.add(anc_dirs_path)
        for cwd, dirs, files in os.walk(dir2):
            for f in dirs + files:
                path = os.path.relpath(os.path.join(cwd, f), dir2)
                right.add(path)
                if f in dirs and path not in left:
                    self._numdirs += 1

        common = left.intersection(right)
        left.difference_update(common)
        right.difference_update(common)

        return DCMP(left, right, common)

    def sync_work(self):
        """Creates new directory if it doesn't exist. Calls to synchronization function. Takes starting and ending
        time."""

        self._starttime = time.time()

        if not os.path.isdir(self._dir2):
            self.log('Creating directory %s' % self._dir2)
            try:
                os.makedirs(self._dir2)
                self._numnewdirs += 1
            except Exception as e:
                self.log(str(e))
                return None

        self.sync()
        self._endtime = time.time()

    def _dowork(self, dir1, dir2, copyfunc=None, updatefunc=None):
        """ Private attribute for doing work.

        :param dir1: the source folder location.
        :param dir2: the replica folder location. Will be created if doesn't exist.
        :param copyfunc: the reference to _copy method of the class.
        :param updatefunc: the reference to _update method of the class.
        """

        self.log('Source directory: %s' % dir1)

        self._dcmp = self._compare(dir1, dir2)

        for f2 in self._dcmp.right_only:
            fullf2 = os.path.join(self._dir2, f2)
            self.log('Deleting %s' % fullf2)
            try:
                if os.path.isfile(fullf2):
                    try:
                        try:
                            os.remove(fullf2)
                        except PermissionError as e:
                            os.chmod(fullf2, stat.S_IWRITE)
                            os.remove(fullf2)
                        self._deleted.append(fullf2)
                        self._numdelfiles += 1
                    except OSError as e:
                        self.log(str(e))
                        self._numdelffld += 1
                elif os.path.isdir(fullf2):
                    try:
                        os.chmod(fullf2, stat.S_IWRITE)
                        shutil.rmtree(fullf2, False)
                        self._deleted.append(fullf2)
                        self._numdeldirs += 1
                    except shutil.Error as e:
                        self.log(str(e))
                        self._numdeldfld += 1

            except Exception as e:
                self.log(str(e))
                continue

        for f1 in self._dcmp.left_only:
            try:
                st = os.stat(os.path.join(self._dir1, f1))
            except os.error:
                continue

            if stat.S_ISREG(st.st_mode):
                if copyfunc:
                    copyfunc(f1, self._dir1, self._dir2)
                    self._added.append(os.path.join(self._dir2, f1))
            elif stat.S_ISDIR(st.st_mode):
                to_make = os.path.join(self._dir2, f1)
                if not os.path.exists(to_make):
                    os.makedirs(to_make)
                    self._numnewdirs += 1
                    self._added.append(to_make)

        for f1 in self._dcmp.common:
            try:
                st = os.stat(os.path.join(self._dir1, f1))
            except os.error:
                continue

            if stat.S_ISREG(st.st_mode):
                if updatefunc:
                    updatefunc(f1, self._dir1, self._dir2)

    def _copy(self, filename, dir1, dir2):
        """ Copies a file from source to replica folder.

        :param filename: the file needed to copy.
        :param dir1: the source folder location.
        :param dir2: the replica folder location.
        """

        rel_path = filename.replace('\\', '/').split('/')
        rel_dir = '/'.join(rel_path[:-1])
        filename = rel_path[-1]

        dir2_root = dir2

        dir1 = os.path.join(dir1, rel_dir)
        dir2 = os.path.join(dir2, rel_dir)

        self.log('Copying file %s from %s to %s' % (filename, dir1, dir2))
        try:
            if not os.path.exists(dir2):
                os.chmod(os.path.dirname(dir2_root), 1911)
                try:
                    os.makedirs(dir2)
                    self._numnewdirs += 1
                except OSError as e:
                    self.log(str(e))
                    self._numdirsfld += 1

            os.chmod(dir2, 1911)

            sourcefile = os.path.join(dir1, filename)
            try:
                if os.path.islink(sourcefile):
                    os.symlink(os.readlink(sourcefile),
                               os.path.join(dir2, filename))
                else:
                    shutil.copy2(sourcefile, dir2)
                self._numfiles += 1
            except (IOError, OSError) as e:
                self.log(str(e))
                self._numcopyfld += 1

        except Exception as e:
            self.log('Error copying file %s' % filename)
            self.log(str(e))

    def _update(self, filename, dir1, dir2):
        """ Updates a file based on difference of content.

        :param filename: the file needed to update.
        :param dir1: the source folder location.
        :param dir2: the replica folder location.
        """

        file1 = os.path.join(dir1, filename)
        file2 = os.path.join(dir2, filename)

        try:
            st1 = os.stat(file1)
            st2 = os.stat(file2)
        except os.error:
            return -1

        need_upd = (not filecmp.cmp(file1, file2, False))
        if need_upd:
            self.log('Updating file %s' % file2)
            try:
                os.chmod(file2, 1638)  # 1638 = 0o666

                try:
                    if os.path.islink(file1):
                        os.symlink(os.readlink(file1), file2)
                    else:
                        try:
                            shutil.copy2(file1, file2)
                        except PermissionError as e:
                            os.chmod(file2, stat.S_IWRITE)
                            shutil.copy2(file1, file2)
                    self._changed.append(file2)
                    self._numcontupdates += 1
                    return 0
                except (IOError, OSError) as e:
                    self.log(str(e))
                    self._numupdsfld += 1
                    return -1

            except Exception as e:
                self.log(str(e))
                return -1

        return -1

    def _dirdiffcopyandupdate(self, dir1, dir2):
        """Synchro function.

        :param dir1: the source folder location.
        :param dir2: the replica folder location.
        """
        self._dowork(dir1, dir2, self._copy, self._update)

    def sync(self):
        """ Sync function. """
        self.log('Synchronizing directory %s with %s' % (self._dir2, self._dir1))
        self._dirdiffcopyandupdate(self._dir1, self._dir2)

    def print_logs(self):
        """ Outputs logs. """
        tt = (str(self._endtime - self._starttime))[:4]

        self.log('%s finished in %s seconds.' % (__pkg_name__, tt))

        self.log('%d directories parsed, %d files copied' %
                 (self._numdirs, self._numfiles))
        if self._numdelfiles:
            self.log('%d files were purged.' % self._numdelfiles)
        if self._numdeldirs:
            self.log('%d directories were purged.' % self._numdeldirs)
        if self._numnewdirs:
            self.log('%d directories were created.' % self._numnewdirs)
        if self._numcontupdates:
            self.log('%d files were updated by content.' % self._numcontupdates)
        if self._numtimeupdates:
            self.log('%d files were updated by timestamp.' % self._numtimeupdates)
        self.log('')  # Break before new synchronization
        if self._numcopyfld:
            self.log('there were errors in copying %d files.'
                     % self._numcopyfld)
        if self._numdirsfld:
            self.log('there were errors in creating %d directories.'
                     % self._numdirsfld)
        if self._numupdsfld:
            self.log('there were errors in updating %d files.'
                     % self._numupdsfld)
        if self._numdeldfld:
            self.log('there were errors in purging %d directories.'
                     % self._numdeldfld)
        if self._numdelffld:
            self.log('there were errors in purging %d files.'
                     % self._numdelffld)
