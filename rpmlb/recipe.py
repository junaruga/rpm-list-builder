import logging

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
        packages = self.recipe['packages']
        for package in packages:
            package_dict = {}
            # String or hash
            if isinstance(package, str):
                package_dict['name'] = package
            elif isinstance(package, dict):
                keys = list(package.keys())
                name = keys[0]
                if not package[name]:
                    raise ValueError('Recipe package %s is invalid format.' %
                                     name)
                package_dict = package[name]
                package_dict['name'] = name
            else:
                raise ValueError('package is invalid.')

            yield package_dict

    def verify(self):
        recipe = self.recipe

        if 'name' not in recipe:
            raise ValueError('name is required in the recipe.')
        if not recipe['name']:
            raise ValueError('name is invalid in the recipe.')

        if 'requires' in recipe:
            if not isinstance(recipe['requires'], list):
                raise ValueError('requires should be a list')

        if 'packages' not in recipe:
            raise ValueError('packages is required in the recipe.')
        if not recipe['packages']:
            raise ValueError('packages is invalid in the recipe.')
        if not isinstance(recipe['packages'], list):
            raise ValueError('packages should be a list.')
        for package_dict in self.each_normalized_package():
            assert(package_dict['name'])

        return True
