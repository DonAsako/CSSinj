"""Tests for the CLI entry point (cssinj.__main__)."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from cssinj.__main__ import main, parse_args

if TYPE_CHECKING:
    from pytest_mock import MockerFixture


def _set_argv(monkeypatch: pytest.MonkeyPatch, *args: str) -> None:
    monkeypatch.setattr(sys, 'argv', ['cssinj', *args])


# --------------------------- parse_args: defaults & types ---------------------------


def test_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    _set_argv(monkeypatch)
    args = parse_args()
    assert args.hostname == '127.0.0.1'
    assert args.port == 5005
    assert args.element == 'input'
    assert args.attribute == 'value'
    assert args.method == 'recursive'
    assert args.timeout == 3.0
    assert args.output is None
    assert args.verbose is False
    assert args.quiet is False
    assert args.details is False
    assert args.no_banner is False
    assert args.log_file is None


def test_custom_values_are_parsed_with_correct_types(monkeypatch: pytest.MonkeyPatch) -> None:
    _set_argv(
        monkeypatch,
        '-H',
        '10.0.0.1',
        '-p',
        '8080',
        '-e',
        'h1',
        '-a',
        'src',
        '-t',
        '1.5',
        '-m',
        'font-face',
    )
    args = parse_args()
    assert args.hostname == '10.0.0.1'
    assert args.port == 8080
    assert isinstance(args.port, int)
    assert args.element == 'h1'
    assert args.attribute == 'src'
    assert args.timeout == 1.5
    assert isinstance(args.timeout, float)
    assert args.method == 'font-face'


def test_log_file_is_parsed_as_path(monkeypatch: pytest.MonkeyPatch) -> None:
    _set_argv(monkeypatch, '--log-file', 'logs/cssinj.log')
    args = parse_args()
    assert isinstance(args.log_file, Path)
    assert str(args.log_file) == 'logs/cssinj.log'


# --------------------------- parse_args: flags & aliases ---------------------------


def test_deprecated_attribut_alias_sets_attribute(monkeypatch: pytest.MonkeyPatch) -> None:
    _set_argv(monkeypatch, '--attribut', 'href')
    assert parse_args().attribute == 'href'


def test_output_flag_defaults_to_output_json_when_bare(monkeypatch: pytest.MonkeyPatch) -> None:
    _set_argv(monkeypatch, '-o')
    assert parse_args().output == 'output.json'


def test_output_flag_accepts_explicit_filename(monkeypatch: pytest.MonkeyPatch) -> None:
    _set_argv(monkeypatch, '-o', 'loot.json')
    assert parse_args().output == 'loot.json'


# --------------------------- parse_args: rejections ---------------------------


def test_version_flag_prints_and_exits_zero(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _set_argv(monkeypatch, '--version')
    with pytest.raises(SystemExit) as exc:
        parse_args()
    assert exc.value.code == 0
    assert capsys.readouterr().out.startswith('cssinj ')


def test_verbose_and_quiet_are_mutually_exclusive(monkeypatch: pytest.MonkeyPatch) -> None:
    _set_argv(monkeypatch, '-v', '-q')
    with pytest.raises(SystemExit) as exc:
        parse_args()
    assert exc.value.code == 2


def test_unknown_method_is_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    """The WIP 'complete' strategy must not be selectable on the CLI."""
    _set_argv(monkeypatch, '-m', 'complete')
    with pytest.raises(SystemExit) as exc:
        parse_args()
    assert exc.value.code == 2


# --------------------------- main() ---------------------------


def test_main_prints_banner_and_starts_injector(
    monkeypatch: pytest.MonkeyPatch,
    mocker: MockerFixture,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _set_argv(monkeypatch)
    mocker.patch('cssinj.__main__.setup_logging')
    injector = mocker.patch('cssinj.__main__.CSSInjector')
    main()
    assert '_____' in capsys.readouterr().out  # banner drawn
    injector.return_value.start.assert_called_once()


def test_main_no_banner_suppresses_banner(
    monkeypatch: pytest.MonkeyPatch,
    mocker: MockerFixture,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _set_argv(monkeypatch, '--no-banner')
    mocker.patch('cssinj.__main__.setup_logging')
    mocker.patch('cssinj.__main__.CSSInjector')
    main()
    assert '_____' not in capsys.readouterr().out


def test_main_details_implies_verbose_logging(
    monkeypatch: pytest.MonkeyPatch,
    mocker: MockerFixture,
) -> None:
    _set_argv(monkeypatch, '--no-banner', '-d')
    setup = mocker.patch('cssinj.__main__.setup_logging')
    mocker.patch('cssinj.__main__.CSSInjector')
    main()
    assert setup.call_args.kwargs['verbose'] is True


def test_main_quiet_is_forwarded_to_logging(
    monkeypatch: pytest.MonkeyPatch,
    mocker: MockerFixture,
) -> None:
    _set_argv(monkeypatch, '--no-banner', '-q')
    setup = mocker.patch('cssinj.__main__.setup_logging')
    mocker.patch('cssinj.__main__.CSSInjector')
    main()
    assert setup.call_args.kwargs['quiet'] is True
    assert setup.call_args.kwargs['verbose'] is False
