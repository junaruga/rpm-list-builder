"""A module to manage a downloader to do nothing."""

import logging

from rpmlb.downloader.base import BaseDownloader

LOG = logging.getLogger(__name__)


class NoneDownloader(BaseDownloader):
    """A downloader class to do nothing."""

    def download(self, package_dict, **kwargs):
        """Override BaseDownloader download method."""
        pass
