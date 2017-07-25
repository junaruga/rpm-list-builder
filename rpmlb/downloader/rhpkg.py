from .base_rpkg import BaseRpkgDownloader


class RhpkgDownloader(BaseRpkgDownloader):
    def command(self):
        return 'rhpkg'
