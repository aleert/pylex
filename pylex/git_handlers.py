# -*- coding: utf-8 -*-

"""
Utilities to download repositories from github.

Note that we use GitPython, which requires Git >1.7.0 installed.
"""
import contextlib
import logging
import os
import shutil
import stat
import sys
from pathlib import Path

from appdirs import user_cache_dir
from git.exc import GitCommandError
from git.remote import RemoteProgress
from git.repo.base import Repo


def download_git_repo(url: str, depth: int = 1) -> Path:
    """Download git repository to a temporary dir."""
    stdout = sys.stdout
    appdir = user_cache_dir('pylex', 'Aleksei Panfilov')
    # clear temp dir from previous run
    try:
        if Path(appdir).exists():
            shutil.rmtree(appdir, onerror=remove_readonly)
        os.makedirs(appdir)
    except PermissionError:
        raise PermissionError('Please, provide access to cache directory at {0}'.format(appdir))

    with contextlib.suppress(FileNotFoundError):
        try:
            Repo.clone_from(url=url, to_path=appdir, depth=depth, progress=Progress(stdout=stdout))
        except GitCommandError:
            logging.error('Couldn\'t download git repository {0}.'.format(url))
            shutil.rmtree(appdir, onerror=remove_readonly)

    return Path(appdir)


class Progress(RemoteProgress):
    """Display download progress."""

    def __init__(self, stdout=None):
        """Add stdout so we can pass it when called from from another file or module."""
        self.stdout = stdout
        super().__init__()

    separate_recieve = True
    separate_resolve = True

    def update(self, op_code, cur_count, max_count=None, message=''):  # noqa: Z213, C901
        """Update status while separating different stages."""
        clear_line = '\u001b[2K'
        cursor_left = '\u001b[1000D'

        self.stdout.write(cursor_left)

        if op_code == 5:
            self.stdout.write('Total files: {0}'.format(max_count))
            self.stdout.write('\n')
            self.stdout.flush()

        elif op_code == RemoteProgress.RECEIVING:
            self.stdout.write(clear_line)
            self.stdout.write('recieving files: {0}/{1} - {2}'.format(
                cur_count,
                max_count,
                message,
            ),
            )
            self.stdout.flush()

        elif op_code == RemoteProgress.RESOLVING:
            if self.separate_recieve:
                self.stdout.write('\n')
                self.separate_recieve = False
            self.stdout.write('resolving deltas: {0}/{1}'.format(cur_count, max_count))
            self.stdout.flush()

        # wonder what that op_code means
        if op_code == 66:  # noqa: Z432
            if self.separate_resolve:
                self.stdout.write('\n')
                self.stdout.flush()
                self.separate_resolve = False


def remove_readonly(func, path, _):
    """Clear the readonly bit and reattempt the removal."""
    os.chmod(path, stat.S_IWRITE)
    func(path)
