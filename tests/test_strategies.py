import argparse
import asyncio

import pytest

from cssinj.strategies import build_strategy, get_strategy, list_strategies
from cssinj.strategies.complete import CompleteStrategy
from cssinj.strategies.fontface import FontFaceStrategy
from cssinj.strategies.recursive import RecursiveStrategy
from cssinj.utils.default import ELEMENTS

from .conftest import ClientFactory


def test_list_strategies_contains_known() -> None:
    assert set(list_strategies()) == {'recursive', 'font-face', 'complete'}


def test_get_strategy_returns_class() -> None:
    assert get_strategy('recursive') is RecursiveStrategy
    assert get_strategy('font-face') is FontFaceStrategy
    assert get_strategy('complete') is CompleteStrategy


def test_get_strategy_unknown_raises() -> None:
    with pytest.raises(ValueError, match='Unknown strategy'):
        get_strategy('does-not-exist')


def test_build_strategy_from_args(cli_args: argparse.Namespace) -> None:
    cli_args.method = 'font-face'
    strategy = build_strategy(cli_args)
    assert isinstance(strategy, FontFaceStrategy)
    assert strategy.hostname == cli_args.hostname
    assert strategy.port == cli_args.port
    assert strategy.element == cli_args.element
    assert strategy.attribute == cli_args.attribute
    assert strategy.timeout == cli_args.timeout


# ---- RecursiveStrategy ----


class TestRecursiveStrategy:
    def test_start_payload_imports_n_route(self, make_client: ClientFactory) -> None:
        c = make_client()
        c.id = 7
        s = RecursiveStrategy(hostname='h', port=1234)
        css = s.generate_start_payload(c)
        assert "@import url('//h:1234/n?" in css
        assert 'cid=7' in css

    def test_handle_valid_replaces_data(self, make_client: ClientFactory) -> None:
        c = make_client()
        s = RecursiveStrategy(hostname='h', port=1)
        s.handle_valid(c, 'abc')
        s.handle_valid(c, 'abcd')
        assert c.data == 'abcd'

    def test_handle_end_appends_element_and_resets_data(self, make_client: ClientFactory) -> None:
        c = make_client()
        c.data = 'secret'
        s = RecursiveStrategy(hostname='h', port=1, element='input', attribute='value')
        body = s.handle_end(c)
        assert body == 'end'
        assert len(c.elements) == 1
        assert c.elements[0].name == 'input'
        assert c.elements[0].attributes[0].name == 'value'
        assert c.elements[0].attributes[0].value == 'secret'
        assert c.data == ''


# ---- FontFaceStrategy ----


class TestFontFaceStrategy:
    def test_start_payload_resets_data_and_clears_ended_flag(self, make_client: ClientFactory) -> None:
        c = make_client()
        c.id = 3
        c.data = 'stale'
        s = FontFaceStrategy(hostname='h', port=1)
        s._ended.add(c.id)
        css = s.generate_start_payload(c)
        assert c.data == ''
        assert c.id not in s._ended
        assert '@font-face' in css
        assert f'cid={c.id}' in css

    def test_handle_valid_accumulates_distinct_chars(self, make_client: ClientFactory) -> None:
        c = make_client()
        s = FontFaceStrategy(hostname='h', port=1)

        async def run() -> None:
            s.handle_valid(c, 'A')
            s.handle_valid(c, 'B')
            s.handle_valid(c, 'A')  # duplicate ignored
            for task in s._timeout_tasks.values():
                task.cancel()

        asyncio.run(run())
        assert c.data == 'AB'

    def test_handle_end_is_idempotent(self, make_client: ClientFactory) -> None:
        """B4 regression: two calls (timer + /e) must not duplicate the Element."""
        c = make_client()
        c.id = 1
        c.data = 'X'
        s = FontFaceStrategy(hostname='h', port=1)
        assert s.handle_end(c) == 'end'
        assert s.handle_end(c) == 'end'
        assert len(c.elements) == 1

    def test_handle_end_cancels_pending_timeout(self, make_client: ClientFactory) -> None:
        c = make_client()
        s = FontFaceStrategy(hostname='h', port=1, timeout=10)

        async def run() -> bool:
            s.handle_valid(c, 'A')
            task = s._timeout_tasks[c.id]
            s.handle_end(c)
            await asyncio.sleep(0)  # let cancellation propagate
            return task.cancelled() or task.done()

        assert asyncio.run(run())

    def test_timeout_triggers_handle_end(self, make_client: ClientFactory) -> None:
        c = make_client()
        c.id = 1
        s = FontFaceStrategy(hostname='h', port=1, timeout=0.02)

        async def run() -> None:
            s.handle_valid(c, 'Z')
            await asyncio.sleep(0.05)

        asyncio.run(run())
        assert c.id in s._ended
        assert any(a.value == 'Z' for el in c.elements for a in el.attributes)


# ---- CompleteStrategy ----


class TestCompleteStrategy:
    def test_start_payload_targets_every_element(self, make_client: ClientFactory) -> None:
        c = make_client()
        c.id = 1
        s = CompleteStrategy(hostname='h', port=1)
        css = s.generate_start_payload(c)
        for name in ELEMENTS:
            assert f'html > {name}:' in css

    def test_next_and_valid_return_constants(self, make_client: ClientFactory) -> None:
        s = CompleteStrategy(hostname='h', port=1)
        c = make_client()
        assert s.generate_next_payload(c) == 'next'
        assert s.handle_valid(c, 'x') == 'valid'

    def test_handle_end_appends_and_resets(self, make_client: ClientFactory) -> None:
        c = make_client()
        c.data = 'x'
        s = CompleteStrategy(hostname='h', port=1)
        assert s.handle_end(c) == 'end'
        assert c.data == ''
        assert len(c.elements) == 1
