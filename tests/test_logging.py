import importlib
import logging
import sys

import pytest


@pytest.fixture
def rpmlb_logging():
    from rpmlb import logging as rpmlb_logging
    yield rpmlb_logging
    # Reset logging module updated by logging.basicConfig.
    importlib.reload(sys.modules['logging'])


def test_configure_logging_logs_on_verbose_false(rpmlb_logging):
    rpmlb_logging.configure_logging(False)
    log = logging.getLogger()
    assert log.getEffectiveLevel() == logging.INFO


def test_configure_logging_logs_on_verbose_true(rpmlb_logging):
    rpmlb_logging.configure_logging(True)
    log = logging.getLogger()
    assert log.getEffectiveLevel() == logging.DEBUG
