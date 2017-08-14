"""A module to manage a common logic for the downloader."""

import logging
import os
import re

from .. import utils

LOG = logging.getLogger(__name__)


class BaseDownloader:
    """A base class for the package downloader."""

    def __init__(self):
        """Initialize this class."""
        pass

    @staticmethod
    def get_instance(name: str):
        """Dynamically instantiate named downloader.

        Inspired from factory method pattern.

        Keyword arguments:
            name: Name of the requested builder.

        Returns:
            Instance of the requested builder.

        """
        class_name = 'rpmlb.downloader.{0}.{1}Downloader'.format(
            name,
            utils.camelize(name)
        )
        instance = utils.get_instance(class_name)

        LOG.debug('Loaded downloader with %s', name)
        return instance

    def run(self, work, **kwargs):
        """Run entire download process.

        before, after, prepare and download methods are run in the method.
        This method is inspired from template method pattern.
        """
        is_resume = kwargs.get('resume', False)
        if is_resume:
            message = (
                'Skip the download process, '
                'because the resume option was used.'
            )
            LOG.info(message)
            return True

        self.before(work, **kwargs)

        for package_dict, num_name in work.each_num_dir():
            if self._is_download_skipped(package_dict, **kwargs):
                name = package_dict['name']
                LOG.debug('Skip download package: %s', name)
                # Create package directory for build process.
                if not os.path.isdir(name):
                    os.mkdir(name)
                continue

            # TODO(Run it with asynchronous)
            self.download(package_dict, **kwargs)

        self.after(work, **kwargs)
        return True

    def before(self, work, **kwargs):
        """Set up for the download logic once.

        This method is intended for setting up the whole download process,
        """
        pass

    def after(self, work, **kwargs):
        """Clean up for the download logic once.

        This method is intended for cleaning up after successful download,
        and it is called once all the work is completed.
        """
        pass

    def download(self, package_dict, **kwargs):
        """Download for given package."""
        raise NotImplementedError('Implement this method.')

    def _is_download_skipped(self, package_dict: dict, **kwargs):
        """Return if skip a download for a pacakge.

        Override if needed.

        Keyword arguments:
            package_dict: A dictionary of package metadata.
            kwargs: option arguments.

        """
        if not package_dict:
            raise ValueError('package_dict is required.')

        is_skipped = False

        dist = kwargs.get('dist')
        if dist and 'dist' in package_dict:
            if not re.match(package_dict['dist'], dist):
                is_skipped = True
        return is_skipped
