"""Test rpmlb.downloader.base_rpkg."""

from unittest import mock

import pytest

from rpmlb.downloader.base_rpkg import BaseRpkgDownloader


@pytest.fixture
def downloader():
    """Return a downloader object."""
    return BaseRpkgDownloader()


@pytest.fixture
def mock_downloader(downloader, monkeypatch):
    """Return a mocked downloader object."""
    monkeypatch.setattr(type(downloader), 'command',
                        mock.PropertyMock(return_value='testpkg'))

    return downloader


def test_init(downloader):
    """Test init is success."""
    assert downloader


def test_command_raises_not_implemented_error(downloader):
    """Test init is success."""
    with pytest.raises(NotImplementedError):
        downloader.command


def test_download_passes_on_valid_arguments(mock_downloader):
    """Test download passes on valid arguments."""
    package_dict = {'name': 'a'}
    branch = 'private-foo'
    with mock.patch('rpmlb.utils.run_cmd',
                    mock.Mock(return_value=True)) as mock_run_cmd:
        mock_downloader.download(package_dict, branch=branch)
        cmd = r'''
testpkg co a && \
cd a && \
git checkout private-foo
        '''.strip()
        mock_run_cmd.assert_called_once_with(cmd)
    assert True


def test_download_raises_error_on_without_package_dict(downloader):
    """Test download raises an error when package_dict is none."""
    package_dict = None
    branch = 'private-foo'
    with mock.patch('rpmlb.utils.run_cmd', mock.Mock(return_value=True)):
        with pytest.raises(ValueError):
            downloader.download(package_dict, branch=branch)


def test_download_raises_error_on_without_branch(downloader):
    """Test download raises an error when branch option is none."""
    package_dict = {'name': 'a'}
    with pytest.raises(ValueError):
        downloader.download(package_dict)
