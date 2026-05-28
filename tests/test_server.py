"""Integration tests for cssinj.exfiltrator.server.Server using pytest-aiohttp."""

from __future__ import annotations

import argparse
import json
from typing import TYPE_CHECKING

from cssinj.client import Clients
from cssinj.exfiltrator.server import Server
from cssinj.file import OutputFile

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable
    from pathlib import Path
    from typing import Any

    import pytest
    from aiohttp.test_utils import TestClient
    from aiohttp.web import Application

    AiohttpClient = Callable[[Application], Awaitable[TestClient[Any, Application]]]


def _make_args(method: str = 'font-face', **overrides: object) -> argparse.Namespace:
    defaults = {
        'hostname': '127.0.0.1',
        'port': 0,
        'element': 'input',
        'attribute': 'value',
        'details': False,
        'method': method,
        'output': None,
        'timeout': 0.05,
    }
    defaults.update(overrides)
    return argparse.Namespace(**defaults)


def _build_server(method: str = 'font-face', output_file: OutputFile | None = None) -> Server:
    return Server(clients=Clients(), args=_make_args(method=method), output_file=output_file)


# --------------------------- Routing & error handling ---------------------------


async def test_unknown_route_returns_404(aiohttp_client: AiohttpClient) -> None:
    srv = _build_server()
    client: TestClient[Any, Application] = await aiohttp_client(srv.app)
    resp = await client.get('/does-not-exist')
    assert resp.status == 404


async def test_unknown_cid_yields_500(aiohttp_client: AiohttpClient) -> None:
    srv = _build_server()
    client = await aiohttp_client(srv.app)
    resp = await client.get('/v', params={'cid': '999', 't': 'A'})
    assert resp.status == 500


async def test_missing_t_param_yields_400(aiohttp_client: AiohttpClient) -> None:
    srv = _build_server()
    client = await aiohttp_client(srv.app)
    await client.get('/start')  # register cid=1
    resp = await client.get('/v', params={'cid': '1'})
    assert resp.status == 400


# --------------------------- /start ---------------------------


async def test_start_registers_client_and_returns_css(aiohttp_client: AiohttpClient) -> None:
    srv = _build_server()
    client = await aiohttp_client(srv.app)
    resp = await client.get('/start')
    assert resp.status == 200
    assert resp.headers['Content-Type'].startswith('text/css')
    body = await resp.text()
    assert '@font-face' in body
    assert len(srv.clients) == 1
    assert srv.clients[0].id == 1


async def test_start_records_request_headers_on_client(aiohttp_client: AiohttpClient) -> None:
    srv = _build_server()
    client = await aiohttp_client(srv.app)
    await client.get('/start', headers={'X-Custom': 'abc'})
    registered = srv.clients[0]
    assert registered.headers.get('X-Custom') == 'abc'


# --------------------------- Font-face full flow ---------------------------


async def test_fontface_full_flow_produces_one_element(aiohttp_client: AiohttpClient) -> None:
    srv = _build_server(method='font-face')
    client = await aiohttp_client(srv.app)
    await client.get('/start')
    await client.get('/v', params={'cid': '1', 't': 'A'})
    await client.get('/v', params={'cid': '1', 't': 'B'})
    resp = await client.get('/e', params={'cid': '1'})
    assert resp.status == 200
    assert (await resp.text()) == 'end'
    [c] = srv.clients
    assert len(c.elements) == 1
    [attr] = c.elements[0].attributes
    assert attr.name == 'textContent'
    assert set(attr.value) == {'A', 'B'}


async def test_fontface_double_end_does_not_duplicate_element(aiohttp_client: AiohttpClient) -> None:
    """B4 regression: timer + /e both calling handle_end must not double-append."""
    srv = _build_server(method='font-face')
    client = await aiohttp_client(srv.app)
    await client.get('/start')
    await client.get('/v', params={'cid': '1', 't': 'X'})
    await client.get('/e', params={'cid': '1'})
    await client.get('/e', params={'cid': '1'})
    assert len(srv.clients[0].elements) == 1


# --------------------------- Recursive ---------------------------


async def test_recursive_start_emits_import(aiohttp_client: AiohttpClient) -> None:
    srv = _build_server(method='recursive')
    client = await aiohttp_client(srv.app)
    resp = await client.get('/start')
    body = await resp.text()
    assert body.startswith("@import url('//")
    assert '/n?' in body


async def test_recursive_handle_end_records_value(aiohttp_client: AiohttpClient) -> None:
    srv = _build_server(method='recursive')
    client = await aiohttp_client(srv.app)
    await client.get('/start')
    await client.get('/v', params={'cid': '1', 't': 'hello'})
    await client.get('/e', params={'cid': '1'})
    [c] = srv.clients
    [el] = c.elements
    [attr] = el.attributes
    assert attr.value == 'hello'
    assert el.name == 'input'


# --------------------------- Output file ---------------------------


async def test_output_file_is_written_during_flow(
    aiohttp_client: AiohttpClient,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    clients = Clients()
    output = OutputFile('out.json', clients)
    srv = Server(clients=clients, args=_make_args(method='recursive'), output_file=output)
    client = await aiohttp_client(srv.app)

    await client.get('/start')
    await client.get('/v', params={'cid': '1', 't': 'secret'})
    await client.get('/e', params={'cid': '1'})

    data = json.loads(output.path.read_text())
    assert data['clients'][0]['elements'][0]['attributes']['value'] == 'secret'
