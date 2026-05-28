"""Shared fixtures."""

from __future__ import annotations

import argparse
import asyncio
from collections.abc import Callable

import pytest

from cssinj.client import Client, Clients

ClientFactory = Callable[..., Client]


@pytest.fixture
def clients() -> Clients:
    return Clients()


@pytest.fixture
def make_client() -> ClientFactory:
    """Factory returning fresh Client instances."""

    def _make(host: str = '1.2.3.4') -> Client:
        return Client(host=host, accept=None, headers={}, event=asyncio.Event())

    return _make


@pytest.fixture
def cli_args() -> argparse.Namespace:
    return argparse.Namespace(
        hostname='127.0.0.1',
        port=0,
        element='input',
        attribute='value',
        details=False,
        method='recursive',
        output=None,
        timeout=0.05,
    )
