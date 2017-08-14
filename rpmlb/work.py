"""A module to manage working directory and the behavior in the directory."""

import logging
import os
import shutil
import tempfile

from rpmlb import utils

LOG = logging.getLogger(__name__)


class Work:
    """A class to manage working directory."""

    def __init__(self, recipe, **kwargs):
        """Initialize this class."""
        if recipe is None:
            raise ValueError('recipe is required.')

        self._recipe = recipe
        max_digit = len(str(recipe.num_of_package))
        self._num_dir_format = '%0{0}d'.format(str(max_digit))

        working_dir = None
        if 'work_directory' in kwargs and kwargs['work_directory']:
            working_dir = kwargs['work_directory']
            if not os.path.exists(working_dir):
                os.makedirs(working_dir)
        else:
            working_dir = tempfile.mkdtemp(prefix='rpmlb-')
        LOG.info('Working directory: %s', working_dir)
        self.working_dir = working_dir

    def close(self):
        """Behave as a deconstructor.

        Remove the working directory.
        """
        if os.path.isdir(self.working_dir):
            shutil.rmtree(self.working_dir)

    def num_name_from_count(self, count):
        """Return number name that is used as number directory.

        The name is the value adding padding zero considering number
        of packages.
        """
        num_name = self._num_dir_format % count
        return num_name

    def each_num_dir(self):
        """Generaror to do something for each number directory.

        Return the package and number directory name,
        staying in each number directory.
        """
        if not os.path.isdir(self.working_dir):
            ValueError('working_dir does not exist.')

        count = 1
        for package_dict in self._recipe.each_normalized_package():
            num_name = self.num_name_from_count(count)
            num_dir = os.path.join(self.working_dir, num_name)

            if not os.path.isdir(num_dir):
                os.makedirs(num_dir)
            with utils.pushd(num_dir):
                yield package_dict, num_name

            count += 1

    def each_package_dir(self):
        """Generaror to do something for each pacakge directory.

        Return the package and number directory name,
        staying in each package directory.
        """
        for package_dict, num_name in self.each_num_dir():
            package = package_dict['name']
            with utils.pushd(package):
                yield package_dict, num_name
