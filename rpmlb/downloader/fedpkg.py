from .base_rpkg import BaseRpkgDownloader


class FedpkgDownloader(BaseRpkgDownloader):
    def command(self):
        return 'fedpkg'
