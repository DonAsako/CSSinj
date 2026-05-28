import json
from pathlib import Path

import pytest

from cssinj.client import Clients
from cssinj.file import File, OutputFile
from cssinj.utils.dom import Attribute, Element

from .conftest import ClientFactory


@pytest.fixture(autouse=True)
def _chdir_tmp(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)


def test_file_does_not_create_on_init() -> None:
    f = File('foo.txt')
    assert not f.path.exists(), 'File() must not write anything until write() is called'


def test_unique_path_preserves_extension() -> None:
    # When 'out.json' exists, the new file must be 'out1.json', not 'out.json1'.
    Path('out.json').write_text('first')
    second = File('out.json')
    assert second.path.name == 'out1.json'
    second.write('x')
    third = File('out.json')
    assert third.path.name == 'out2.json'


def test_unique_path_for_extensionless_file() -> None:
    Path('log').write_text('x')
    f = File('log')
    assert f.path.name == 'log1'
    f.write('y')
    assert File('log').path.name == 'log2'


def test_write_persists_content() -> None:
    f = File('data.txt')
    f.write('hello')
    assert f.path.read_text() == 'hello'


def test_outputfile_serializes_clients(make_client: ClientFactory) -> None:
    clients = Clients()
    c = clients.register(make_client())
    el = Element(name='input')
    el.attributes.append(Attribute(name='value', value='secret'))
    c.elements.append(el)

    out = OutputFile('data.json', clients)
    out.update()

    payload = json.loads(out.path.read_text())
    assert payload == {
        'clients': [
            {
                'id': c.id,
                'headers': {},
                'elements': [{'id': el.id, 'name': 'input', 'attributes': {'value': 'secret'}}],
            },
        ],
    }


def test_outputfile_skips_attributes_key_when_empty(make_client: ClientFactory) -> None:
    clients = Clients()
    c = clients.register(make_client())
    c.elements.append(Element(name='div'))

    out = OutputFile('data.json', clients)
    out.update()

    payload = json.loads(out.path.read_text())
    assert 'attributes' not in payload['clients'][0]['elements'][0]
