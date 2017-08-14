"""A module to manage YAML data in rpmlb."""

import logging
import os

import yaml

from . import utils

LOG = logging.getLogger(__name__)


class Yaml:
    """A class to manage YAML data."""

    def __init__(self, file_path):
        """Initialize this class."""
        try:
            from yaml import CLoader as Loader
        except ImportError:
            from yaml import Loader
        try:
            with open(str(file_path), 'r') as stream:
                self.content = yaml.load(stream, Loader=Loader)
        except FileNotFoundError as e:
            LOG.error('File not found: %s at %s', file_path, os.getcwd())
            raise e

    def dump(self):
        """Print a dump data of the yaml data."""
        try:
            from yaml import CDumper as Dumper
        except ImportError:
            from yaml import Dumper
        output = yaml.dump(self.content, Dumper=Dumper,
                           default_flow_style=False)
        print(output)

    @staticmethod
    def run_cmd_element(cmd_element, **kwargs):
        """Run shell command for the cmd_element.

        cmd_element: Command object. str or list object is available.
        """
        if isinstance(cmd_element, str):
            cmds = [cmd_element]
        elif isinstance(cmd_element, list):
            cmds = cmd_element
        else:
            message = 'Invalid type of cmd_element: {!r}'.format(
                type(cmd_element)
            )
            raise ValueError(message)
        for cmd in cmds:
            utils.run_cmd(cmd, **kwargs)
