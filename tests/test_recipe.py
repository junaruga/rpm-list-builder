"""Test rpmlb.recipe."""

from collections import defaultdict
from collections.abc import Mapping

import pytest

from rpmlb.recipe import Recipe, RecipeError


@pytest.fixture
def ok_recipe(valid_recipe_path):
    """Return valid Recipe object."""
    return Recipe(str(valid_recipe_path), 'rh-ror50')


@pytest.fixture
def invalid_pkg_type():
    """Return a package entry of invalid type."""
    return float('nan')  # anything but str or Mapping


@pytest.fixture
def invalid_pkg_content():
    """Return a package entry with an invalid content."""
    return {'pkg-a': {}, 'pkg-b': {}}


@pytest.fixture
def invalid_recipe(ok_recipe, invalid_pkg_type, invalid_pkg_content):
    """Return Recipe object with invalid package contents."""
    ok_recipe.recipe['packages'] += [
        invalid_pkg_content,
        invalid_pkg_type,
    ]

    return ok_recipe


@pytest.fixture
def bootstrap_recipe(ok_recipe):
    """Return Recipe object with multiple packages that need bootstrapping."""
    ok_recipe.recipe['packages'] += [
        'pkg-a', 'pkg-b',
        'pkg-a', 'pkg-b',
        'pkg-a', 'pkg-b',
    ]

    return ok_recipe


def test_init(ok_recipe):
    """Test init is success."""
    assert ok_recipe


def test_recipe(ok_recipe):
    """Test recipe property is valid."""
    assert ok_recipe.recipe


def test_recipe_not_found(valid_recipe_path):
    """Test to raise error when the collection ID is not found."""
    with pytest.raises(KeyError):
        Recipe(str(valid_recipe_path), 'dummy')


def test_verify_returns_true_on_valid_recipe(ok_recipe):
    """Test verify is success for valid recipe data."""
    assert ok_recipe.verify()


def test_verify_returns_true_on_recipe_with_name(ok_recipe):
    """Test verify is success on a recipe with name."""
    ok_recipe.recipe['name'] = 'a'
    assert ok_recipe.verify()


def test_verify_raises_error_on_recipe_with_empty_name(ok_recipe):
    """Test verify raises an error on a recipe with empty name."""
    ok_recipe.recipe['name'] = ''
    with pytest.raises(RecipeError):
        ok_recipe.verify()


def test_verify_raises_error_on_recipe_with_invalid_name(ok_recipe):
    """Test verify raises an error on the name type is invalid."""
    ok_recipe.recipe['name'] = ['a']
    with pytest.raises(RecipeError):
        ok_recipe.verify()


def test_verify_returns_true_on_recipe_with_requires(ok_recipe):
    """Test verify is success a recipe with requires element."""
    ok_recipe.recipe['requires'] = [
        'rh-ruby23', 'rh-nodejs4', 'rh-mongodb32',
    ]
    assert ok_recipe.verify()


def test_verify_raises_error_on_recipe_with_non_list_requires(ok_recipe):
    """Test verify raises an error on the requires type is invalid."""
    ok_recipe.recipe['requires'] = 'abc'
    with pytest.raises(RecipeError):
        ok_recipe.verify()


def test_verify_raises_error_on_recipe_without_packages(ok_recipe):
    """Test verify raises an error on a recipe without packages."""
    del ok_recipe.recipe['packages']
    with pytest.raises(RecipeError):
        ok_recipe.verify()


def test_verify_raises_error_on_recipe_with_empty_packages(ok_recipe):
    """Test verify raises an error on a recipe with empty packages."""
    ok_recipe.recipe['packages'] = []
    with pytest.raises(RecipeError):
        ok_recipe.verify()


def test_verify_raises_error_on_recipe_with_non_list_packages(ok_recipe):
    """Test verify raises an error on the packages type is invalid."""
    ok_recipe.recipe['packages'] = 'abc'
    with pytest.raises(RecipeError):
        ok_recipe.verify()


def test_verify_raises_error_on_recipe_with_empty_package_name(ok_recipe):
    """Test verify raises an error with empty package name."""
    ok_recipe.recipe['packages'] = [
        'foo',
        ''
    ]
    with pytest.raises(RecipeError):
        ok_recipe.verify()


def test_verify_raises_error_on_recipe_with_unknown_element(ok_recipe):
    """Test verify raises an error on recipe with unknown element."""
    ok_recipe.recipe['unknown'] = 'a'
    with pytest.raises(RecipeError):
        ok_recipe.verify()


@pytest.mark.parametrize('key', ('macros', 'replaced_macros', 'cmd', 'dist'))
def test_verify_raises_error_with_empty_value_in_package(ok_recipe, key):
    """Test verify raises an error with the empty value in the package."""
    package = {
        'foo_package': {
            key: ''
        }
    }
    ok_recipe.recipe['packages'].append(package)

    with pytest.raises(RecipeError):
        ok_recipe.verify()


@pytest.mark.parametrize('key', ('macros', 'replaced_macros'))
def test_verify_raises_error_with_invalid_macros_in_package(ok_recipe, key):
    """Test verify raises an error with invalid macros in the package."""
    package = {
        'foo_package': {
            key: ['a']
        }
    }
    ok_recipe.recipe['packages'].append(package)

    with pytest.raises(RecipeError):
        ok_recipe.verify()


def test_verify_raises_error_with_invalid_cmd_in_package(ok_recipe):
    """Test verify raises an error when the cmd type is invalid."""
    package = {
        'foo_package': {
            'cmd': {
                'a': 'cmd_a',
                'b': 'cmd_b',
            }
        }
    }

    ok_recipe.recipe['packages'].append(package)

    with pytest.raises(RecipeError):
        ok_recipe.verify()


def test_verify_raises_error_with_invalid_dist_in_package(ok_recipe):
    """Test verify raises an error when the dist type is invalid."""
    package = {
        'foo_package': {
            'dist': ['el6', 'el7']
        }
    }

    ok_recipe.recipe['packages'].append(package)

    with pytest.raises(RecipeError):
        ok_recipe.verify()


def test_verify_raises_error_with_unknown_element_in_package(ok_recipe):
    """Test verify raises an error when there is an unknown element."""
    package = {
        'foo_package': {
            'unknown': 'a',
        }
    }

    ok_recipe.recipe['packages'].append(package)

    with pytest.raises(RecipeError):
        ok_recipe.verify()


def test_verify_raises_error_with_multi_key_in_package(ok_recipe):
    """Test verify raises an error with multi keys in the package."""
    package = {
        'foo_package': {
            'cmd': 'ls'
        },
        'bar_package': {
            'cmd': 'ls'
        }
    }

    ok_recipe.recipe['packages'].append(package)

    with pytest.raises(RecipeError):
        ok_recipe.verify()


def test_verify_raises_error_with_invalid_package_type(ok_recipe):
    """Test verify raises an error when the package type is invalid."""
    package = ['foo_package', 'a']

    ok_recipe.recipe['packages'].append(package)

    with pytest.raises(RecipeError):
        ok_recipe.verify()


def test_verify_recipe_returns_messages_on_error(ok_recipe):
    """Test verify returns messages on an error."""
    a_package = {
        'a_package': {
            'macros': 'a',
            'patch': 'ls'
        }
    }
    ok_recipe.recipe['packages'].append(a_package)
    messages = ok_recipe._verify_recipe()
    assert len(messages) == 2


def test_verify_recipe_returns_empty_messages_on_success(ok_recipe):
    """Test verify_recipe returns empty message on a success."""
    a_package = {
        'a_package': {
            'macros': {
                'a': 'A'
            },
            'dist': 'fc23'
        }
    }
    ok_recipe.recipe['packages'].append(a_package)
    messages = ok_recipe._verify_recipe()
    assert len(messages) == 0


def test_verify_packages_raises_error_on_messages_none(ok_recipe):
    """Test verify_packages_and_append raises error.

    when input messages object are none.

    """
    messages = None
    packages = ['a']
    with pytest.raises(ValueError):
        ok_recipe._verify_packages_and_append(messages, packages)


def test_verify_packages_returns_on_empty_messages(ok_recipe):
    """Test verify_packages_and_append is success.

    when input messages object is empty.

    """
    messages = []
    packages = ['a']
    out_messages = ok_recipe._verify_packages_and_append(messages, packages)
    assert len(out_messages) == 0


def test_verify_packages_raises_error_on_packages_none(ok_recipe):
    """Test verify_packages_and_append raises error.

    when input packages object is none.

    """
    messages = ['a']
    packages = None
    with pytest.raises(ValueError):
        ok_recipe._verify_packages_and_append(messages, packages)


def test_verify_packages_metadata_raises_error_on_messages_none(ok_recipe):
    """Test verify_packages_and_append raises error.

    when input messages object is none.

    """
    messages = None
    metadata = ['a']
    disp_package = 'a'
    with pytest.raises(ValueError):
        ok_recipe._verify_packages_metadata_and_append(
            messages, metadata, disp_package)


def test_verify_packages_metadata_raises_error_on_metadata_none(ok_recipe):
    """Test verify_packages_and_append raises error.

    when input metadata object is none.

    """
    messages = ['a']
    metadata = None
    disp_package = 'a'
    with pytest.raises(ValueError):
        ok_recipe._verify_packages_metadata_and_append(
            messages, metadata, disp_package)


def test_verify_packages_metadata_raises_error_on_disp_package_none(ok_recipe):
    """Test verify_packages_metadata_and_append raises an error.

    when inpt disp_package is none.

    """
    messages = ['a']
    metadata = {
        'cmd': 'ls'
    }
    disp_package = None
    with pytest.raises(ValueError):
        ok_recipe._verify_packages_metadata_and_append(
            messages, metadata, disp_package)


def test_package_name_type_checks(ok_recipe):
    """Test invalid package types are reported."""
    invalid_type = float('nan')
    with pytest.raises(ValueError):
        ok_recipe._package_name(invalid_type)

    valid_type = 'pkg-a'
    name = ok_recipe._package_name(valid_type)
    assert name == 'pkg-a'

    invalid_contents = {'pkg-a': {}, 'pkg-b': {}}
    with pytest.raises(ValueError):
        ok_recipe._package_name(invalid_contents)

    valid_contents = {'pkg-a': {}}
    name = ok_recipe._package_name(valid_contents)
    assert name == 'pkg-a'


def test_package_normalization_type_checks(invalid_recipe):
    """Test invalid packages are reported when normalizing."""
    with pytest.raises(ValueError):
        list(invalid_recipe.each_normalized_package())


def test_package_normalization_raises_error_on_invalid_dict(ok_recipe):
    """Test each_normalized_package raises error.

    with invalid pacakge in packages.
    """
    package = {
        'a_package': {
            'macros': {
                'a': 'A'
            }
        },
        'b_package': {
            'macros': {
                'a': 'A'
            }
        }
    }
    ok_recipe.recipe['packages'].append(package)

    with pytest.raises(ValueError):
        list(ok_recipe.each_normalized_package())


def test_normalized_packages_have_expected_format(ok_recipe):
    """Test after normalization, all packages have expected format."""
    a_package = {
        'a_package': {
            'macros': {
                'a': 'A'
            },
            'replaced_macros': {
                'b': 'B'
            },
        }
    }
    ok_recipe.recipe['packages'].append(a_package)

    def valid_item(package: Mapping, key: str, types: tuple):
        """Check validity of a package metadata item."""
        exists = key in package
        value = package.get(key, None)
        valid_type = isinstance(value, types)

        return exists and valid_type

    all_packages = list(ok_recipe.each_normalized_package())
    packages_with_macros = [pkg for pkg in all_packages if 'macros' in pkg]
    packages_with_replaced_macros = [
        pkg for pkg in all_packages if 'replaced_macros' in pkg
    ]

    # Each package has a name
    assert all('name' in pkg for pkg in all_packages), all_packages

    # Each package has bootstrap position of correct type
    key_types = 'bootstrap_position', (type(None), int)
    assert all(valid_item(pkg, *key_types) for pkg in all_packages), \
        all_packages

    # Each macros value is a mapping
    key_types = 'macros', (Mapping,)
    assert all(valid_item(pkg, *key_types) for pkg in packages_with_macros), \
        packages_with_macros

    # Each replaced_macros value is a mapping
    key_types = 'replaced_macros', (Mapping,)
    assert all(
        valid_item(pkg, *key_types)
        for pkg in packages_with_replaced_macros
    ), packages_with_replaced_macros


def test_bootstrap_sequence_increments_correctly(bootstrap_recipe):
    """Test packages that needs bootstrapping are correctly marked as such."""
    sequences = defaultdict(list)
    for pkg in bootstrap_recipe.each_normalized_package():
        sequences[pkg['name']].append(pkg['bootstrap_position'])

    assert sequences['pkg-a'] == [1, 2, None], sequences['pkg-a']
