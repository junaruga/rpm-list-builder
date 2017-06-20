import logging
import os
import yaml
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader
try:
    from yaml import CDumper as Dumper
except ImportError:
    from yaml import Dumper

LOG = logging.getLogger(__name__)


def load(file_path):
    try:
        obj = None
        with open(file_path, 'r') as stream:
            obj = yaml.load(stream, Loader=Loader)
        return obj
    except FileNotFoundError as e:
        LOG.error('File not found: %s at %s', file_path, os.getcwd())
        raise e

def dump(obj):
    output = yaml.dump(obj, Dumper=Dumper,
                       default_flow_style=False)
    print(output)
