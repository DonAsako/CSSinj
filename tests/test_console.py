import logging

import pytest

from cssinj.console import LOGGER_NAME, Console, LogLevel, setup_logging


def test_log_levels_have_emoji_and_logging_level() -> None:
    for lvl in LogLevel:
        assert isinstance(lvl.emoji, str)
        assert lvl.level in (logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR)


def test_setup_logging_is_idempotent() -> None:
    setup_logging()
    n = len(logging.getLogger(LOGGER_NAME).handlers)
    setup_logging()
    assert len(logging.getLogger(LOGGER_NAME).handlers) == n


def test_quiet_overrides_verbose() -> None:
    setup_logging(quiet=True, verbose=True)
    assert logging.getLogger(LOGGER_NAME).level == logging.WARNING


def test_verbose_sets_debug() -> None:
    setup_logging(verbose=True)
    assert logging.getLogger(LOGGER_NAME).level == logging.DEBUG


def test_default_is_info() -> None:
    setup_logging()
    assert logging.getLogger(LOGGER_NAME).level == logging.INFO


def _attach_caplog(caplog: pytest.LogCaptureFixture) -> None:
    """setup_logging sets propagate=False, so caplog's root handler never sees us.
    Attach its handler directly to the cssinj logger instead."""
    logging.getLogger(LOGGER_NAME).addHandler(caplog.handler)


def test_log_writes_through_logging(caplog: pytest.LogCaptureFixture) -> None:
    setup_logging(verbose=True)
    _attach_caplog(caplog)
    caplog.set_level(logging.DEBUG, logger=LOGGER_NAME)
    Console.log(LogLevel.EXFILTRATION, 'hello')
    record = next(r for r in caplog.records if 'hello' in r.message)
    assert record.levelno == logging.DEBUG
    assert getattr(record, 'emoji', None) == LogLevel.EXFILTRATION.emoji


def test_error_handler_attaches_context(caplog: pytest.LogCaptureFixture) -> None:
    setup_logging()
    _attach_caplog(caplog)
    caplog.set_level(logging.ERROR, logger=LOGGER_NAME)
    Console.error_handler(ValueError('boom'), context={'path': '/v', 'cid': '1'})
    msg = caplog.records[-1].message
    assert 'boom' in msg
    assert 'path=/v' in msg
    assert 'cid=1' in msg
