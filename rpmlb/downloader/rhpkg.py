"""A module for a downloader with rhpkg command."""

from .base_rpkg import BaseRpkgDownloader


class RhpkgDownloader(BaseRpkgDownloader):
    """A downloader class to get a pacakge with rhpkg command."""

    """Override BaseRpkgDownloader command property."""
    command = 'rhpkg'
