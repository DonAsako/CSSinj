"""Tests for the CSSInjector orchestrator (cssinj.exfiltrator.cssinjector)."""

from __future__ import annotations

import argparse
from typing import TYPE_CHECKING

from cssinj.exfiltrator.cssinjector import CSSInjector

if TYPE_CHECKING:
    from pathlib import Path

    import pytest
    from pytest_mock import MockerFixture

_INJECTOR_MOD = 'cssinj.exfiltrator.cssinjector'


def _args(**overrides: object) -> argparse.Namespace:
    base: dict[str, object] = {
        'hostname': '127.0.0.1',
        'port': 0,
        'element': 'input',
        'attribute': 'value',
        'details': False,
        'method': 'recursive',
        'output': None,
        'timeout': 0.05,
    }
    base.update(overrides)
    return argparse.Namespace(**base)


def test_start_without_output_runs_server_and_creates_no_file(mocker: MockerFixture) -> None:
    server = mocker.patch(f'{_INJECTOR_MOD}.Server')
    run = mocker.patch(f'{_INJECTOR_MOD}.asyncio.run')

    injector = CSSInjector()
    injector.start(_args())

    assert injector.output_file is None
    server.assert_called_once()
    assert server.call_args.kwargs['output_file'] is None
    run.assert_called_once()


def test_start_with_output_creates_output_file_and_passes_it_to_server(
    mocker: MockerFixture,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    server = mocker.patch(f'{_INJECTOR_MOD}.Server')
    mocker.patch(f'{_INJECTOR_MOD}.asyncio.run')

    injector = CSSInjector()
    injector.start(_args(output='loot.json'))

    assert injector.output_file is not None
    assert server.call_args.kwargs['output_file'] is injector.output_file
    # OutputFile must not write anything until an update() is triggered.
    assert not injector.output_file.path.exists()


def test_start_suppresses_keyboard_interrupt(mocker: MockerFixture) -> None:
    mocker.patch(f'{_INJECTOR_MOD}.Server')
    mocker.patch(f'{_INJECTOR_MOD}.asyncio.run', side_effect=KeyboardInterrupt)

    injector = CSSInjector()
    injector.start(_args())  # must not raise
