import pytest

from rpmlb import yaml


def test_load_returns_object():
    obj = yaml.load('tests/fixtures/recipes/ror.yml')
    assert(obj)


def test_load_raises_error_when_fails_to_open_file():
    file_path = 'dummy'
    with pytest.raises(FileNotFoundError):
        yaml.load(file_path)


def test_dump(capsys):
    obj = {
        'a': 'b',
        'c': ['d', 'e']
    }
    yaml.dump(obj)
    stdout, stderr = capsys.readouterr()
    assert stdout == 'aaa'
