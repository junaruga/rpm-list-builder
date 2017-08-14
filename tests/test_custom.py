"""Test rpmlb.custom."""

from unittest import mock

import pytest

from rpmlb.custom import Custom


@pytest.fixture
def valid_custom(valid_custom_file_path):
    """Return a custom object with a valid custom file."""
    return Custom(valid_custom_file_path)


def test_init_loads_file(valid_custom):
    """Test that init loads file."""
    assert valid_custom


def test_run_cmds_runs_cmds_on_valid_custom_file(valid_custom, monkeypatch):
    """Test run_cmds is success with valid custom file."""
    with pytest.helpers.generate_tmp_path_list(2) as tmp_paths:
        random_file_foo, random_file_bar_part = tmp_paths

        content = {
            'build': [
                'touch {0!s}'.format(random_file_foo),
                'touch "{0!s}-$PKG"'.format(random_file_bar_part),
            ]
        }
        monkeypatch.setattr(type(valid_custom), 'yaml_content',
                            mock.PropertyMock(return_value=content))

        valid_custom.run_cmds('build', name='rubygem-bar')

        random_file_bar = random_file_bar_part.with_name(
            random_file_bar_part.name + '-rubygem-bar'
        )

        assert random_file_foo.is_file()
        assert random_file_bar.is_file()


def test_run_cmds_skips_cmds_on_unknown_key(valid_custom, random_file_path,
                                            monkeypatch):
    """Test run_cmds skips commands on known key."""
    content = {
        'build': [
            'touch {0!s}'.format(random_file_path),
        ]
    }
    monkeypatch.setattr(type(valid_custom), 'yaml_content',
                        mock.PropertyMock(return_value=content))

    valid_custom.run_cmds('dummy')

    assert not random_file_path.is_file()


def test_yaml_content_returns_content(valid_custom):
    """Test to return valid YAML content."""
    content = valid_custom.yaml_content
    assert content


def test_yaml_content_returns_singleton_object(valid_custom):
    """Test content returns singleton object."""
    content = valid_custom.yaml_content
    content2 = valid_custom.yaml_content
    assert content is content2
