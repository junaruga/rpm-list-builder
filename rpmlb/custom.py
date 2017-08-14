"""A module to manage custom file."""

import logging
import os.path

from rpmlb.yaml import Yaml

LOG = logging.getLogger(__name__)


class Custom:
    """A class to manage custom file."""

    def __init__(self, file_path):
        """Initialize the class."""
        self._file_path = file_path = os.path.abspath(str(file_path))
        self._custom_dir = os.path.dirname(file_path)
        self._yaml_content = None

    def run_cmds(self, key, **kwargs):
        """Run commands in a custom file.

        Reserved environment variables
        PKG: Package name.
        CUSTOM_DIR: The directory that the custom file exists in.
        """
        env = {}
        # Support environment variable to use PKG as pacakge name in the file.
        if 'name' in kwargs:
            env['PKG'] = kwargs['name']

        cmd_dict = self.yaml_content
        if key not in cmd_dict:
            return
        cmd_element = cmd_dict[key]

        env['CUSTOM_DIR'] = self._custom_dir
        Yaml.run_cmd_element(cmd_element, env=env)

    @property
    def yaml_content(self):
        """Load cutome file's content from the file path.

        Singleton method.
        """
        if self._yaml_content:
            return self._yaml_content
        yaml = Yaml(self._file_path)
        self._yaml_content = yaml.content
        return self._yaml_content
