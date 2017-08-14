"""A module for a downloader with fedpkg command."""

from .base_rpkg import BaseRpkgDownloader


class FedpkgDownloader(BaseRpkgDownloader):
    """A downloader class to get a pacakge with fedpkg command."""

    """Override BaseRpkgDownloader command property."""
    command = 'fedpkg'
