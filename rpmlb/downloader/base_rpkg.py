"""A module for a downloader with package command."""

import logging

from .. import utils
from .base import BaseDownloader

LOG = logging.getLogger(__name__)


class BaseRpkgDownloader(BaseDownloader):
    """A downloader class to get a pacakge with package command."""

    @property
    def command(self):
        """Return the package command name.

        Excepted to implement this method in the sub class.
        """
        raise NotImplementedError('Implement this method.')

    def download(self, package_dict, **kwargs):
        """Override BaseDownloader download method."""
        if not package_dict:
            raise ValueError('package_dict is required.')
        if 'branch' not in kwargs or not kwargs['branch']:
            raise ValueError('branch is required.')
        branch = kwargs['branch']

        package = package_dict['name']
        cmd = r'''
{} co {} && \
cd {} && \
git checkout {}
        '''.strip().format(self.command, package, package, branch)
        utils.run_cmd(cmd)
