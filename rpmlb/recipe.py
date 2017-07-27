import logging
from collections import Counter
from itertools import starmap
from typing import Iterator, Mapping, Union

from rpmlb.yaml import Yaml

LOG = logging.getLogger(__name__)


class Recipe:
    """A class to describe recipe data."""

    def __init__(self, file_path, collection_id):
        if not file_path:
            raise ValueError('file_path is required.')
        if not collection_id:
            raise ValueError('collection_id is required.')

        self._collection_id = collection_id

        yaml = Yaml(file_path)
        LOG.debug('Loaded recipe: %s', file_path)
        recipe_dict = yaml.content
        self.recipe = recipe_dict[collection_id]
        self.num_of_package = len(self.recipe['packages'])

    def each_normalized_package(self):
        """Present recipe packages in normalized form.

        Yields:
            Dictionary with the package's data.

        Common keys in the yielded dictionary:
            - name: The package's name
            - bootstrap_position: Numerical position in the bootstrapping
                sequence, or None if no bootstrap is necessary.
            - macros, replaced_macros: Mapping of macro name to (new)
                macro body.
        """

        packages = self.recipe['packages']
        bootstrap_map = self._count_bootstrap_sequences()

        for package in packages:
            name = self._package_name(package)
            bootstrap_position = next(bootstrap_map[name], None)

            package_dict = {
                'name': name,
                'bootstrap_position': bootstrap_position,
            }

            if isinstance(package, Mapping):
                # package should be one-item dictionary
                if len(package) != 1:
                    message = 'Invalid package data: {}'.format(package)
                    raise ValueError(message)

                metadata, = package.values()
                package_dict.update(metadata)

            yield package_dict

    def verify(self):
        recipe = self.recipe

        if 'packages' not in recipe:
            raise ValueError('packages is required.')
        if not recipe['packages']:
            raise ValueError('packages is empty.')
        if not isinstance(recipe['packages'], list):
            raise ValueError('packages should be a list.')

        for recipe_key in recipe:
            if recipe_key == 'name':
                if not recipe[recipe_key]:
                    raise ValueError('{0} is empty.'.
                                     format(recipe_key))

                if not isinstance(recipe[recipe_key], str):
                    raise ValueError('{0} shoule be a string.'.
                                     format(recipe_key))
            elif recipe_key == 'requires':
                if not recipe[recipe_key]:
                    raise ValueError('{0} is empty.'.
                                     format(recipe_key))
                if not isinstance(recipe[recipe_key], list):
                    raise ValueError('{0} should be a list.'.
                                     format(recipe_key))
            elif recipe_key == 'packages':
                pass
            else:
                raise ValueError(
                    'Unknown element {0} exists.'.
                    format(recipe_key))

        for package_dict in self.each_normalized_package():
            name = package_dict['name']
            if not name:
                raise ValueError('name is empty in the package.')

            for key in package_dict.keys():
                if key == 'name':
                    pass
                elif key in {'macros', 'replaced_macros'}:
                    if not package_dict[key]:
                        raise ValueError('{0} is empty in the pacakge: {1}.'.
                                         format(key, name))

                    if not isinstance(package_dict[key], dict):
                        raise ValueError(
                            '{0} should be a hash in the package: {1}.'.
                            format(key, name))
                elif key == 'cmd':
                    if not package_dict[key]:
                        raise ValueError('{0} is empty in the package: {1}.'.
                                         format(key, name))
                    if not isinstance(package_dict[key], (str, list)):
                        message_format = (
                            '{0} should be a string '
                            'or a list in the package: {1}.'
                        )
                        raise ValueError(message_format.format(key, name))
                elif key == 'dist':
                    if not package_dict[key]:
                        raise ValueError('{0} is empty in the package: {1}.'.
                                         format(key, name))
                    if not isinstance(package_dict[key], str):
                        raise ValueError(
                            '{0} should be a string in the package: {1}.'.
                            format(key, name))
                elif key == 'bootstrap_position':
                    pass
                else:
                    raise ValueError(
                        'Unknown element {0} exists in the package: {1}.'.
                        format(key, name))

        return True

    @staticmethod
    def _package_name(package: Union[str, dict]) -> str:
        """Extract package name.

        Keyword arguments:
            package: Raw package data to analyze.
                It should be either string or one-item dictionary.

        Returns:
            Name of the package.

        Raises:
            ValueError: Invalid package type.
        """

        if isinstance(package, str):  # The name itself
            return package

        elif isinstance(package, dict):
            # package should be one-item dictionary
            if len(package) != 1:
                message = 'Invalid package data: {}'.format(package)
                raise ValueError(message)

            # The name is the only key
            name, = package.keys()
            return name

        else:
            message = 'Invalid type of package: {!r}'.format(type(package))
            raise ValueError(message)

    def _count_bootstrap_sequences(self) -> Mapping[str, Iterator[int]]:
        """Count package instances and produce bootstrap sequences.

        Returns:
            Mapping of package number to iterator of bootstrap numbers.
        """

        name_list = map(self._package_name, self.recipe['packages'])
        count_map = Counter(name_list)

        def make_sequence(name: str, count: int):
            """Count package instances except the last one; start from 1"""

            sequence = range(1, count)
            return name, iter(sequence)

        # Create a dictionary from (name, sequence) tuples
        sequence_map = dict(starmap(make_sequence, count_map.items()))

        return sequence_map
