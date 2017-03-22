import logging

# from sclh import utils

LOG = logging.getLogger(__name__)


class BaseDownloader(object):
    """A base class for the package downloader."""

    def __init__(self):
        pass

    @classmethod
    def get_instance(cls, name):
        # TODO: Use reflection.
        # class_name = 'sclh.downloader.{0}.{1}Downloader'.format(
        #     name,
        #     utils.camelize(name)
        # )
        # return utils.get_instance(class_name)
        instance = None
        if name == 'local':
            from sclh.downloader.local import LocalDownloader
            instance = LocalDownloader()
        elif name == 'rhpkg':
            from sclh.downloader.rhpkg import RhpkgDownloader
            instance = RhpkgDownloader()
        elif name == 'none':
            from sclh.downloader.none import NoneDownloader
            instance = NoneDownloader()
        else:
            raise ValueError('name is invalid.')
        return instance

    def run(self, work, **kwargs):
        for package_dict in work.each_num_dir():
            # TODO(Run it with asynchronous)
            self.download(package_dict, **kwargs)
        return True

    def download(self, package_dict, **kwargs):
        raise NotImplementedError('Implement this method.')