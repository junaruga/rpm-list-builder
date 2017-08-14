"""A module for the dummy builder."""

import logging

from rpmlb.builder.base import BaseBuilder

LOG = logging.getLogger(__name__)


class DummyBuilder(BaseBuilder):
    """A dummy builder class."""

    def build(self, package_dict, **kwargs):
        """Override BaseBuilder build method.

        Only output log for the dummy build.
        """
        LOG.info('dummy build %s', package_dict['name'])
