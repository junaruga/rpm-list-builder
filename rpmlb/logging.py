import logging

""" Set log format considering
lavelname:
    DEBUG: 5
    INFO: 4
    WARNING: 7
    ERROR: 5
    CRITICAL: 8
name: module name
"""
LOG_FORMAT = '%(asctime)s %(levelname)-8s %(name)-26s %(message)s'


def configure_logging(verbose):
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=log_level, format=LOG_FORMAT)

    log = logging.getLogger(__name__)
    log.debug('Added logging handler to logger root at %s', __name__)
