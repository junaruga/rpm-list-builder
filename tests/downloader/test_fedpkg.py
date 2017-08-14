"""Test rpmlb.downloader.rhpkg."""

from rpmlb.downloader.fedpkg import FedpkgDownloader


def test_command_returns_the_value():
    """Test command property returns the value."""
    downloader = FedpkgDownloader()
    assert downloader.command == 'fedpkg'
