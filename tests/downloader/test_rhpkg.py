"""Test rpmlb.downloader.rhpkg."""

from rpmlb.downloader.rhpkg import RhpkgDownloader


def test_command_returns_the_value():
    """Test command property returns the value."""
    downloader = RhpkgDownloader()
    assert downloader.command == 'rhpkg'
