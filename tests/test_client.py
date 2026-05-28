import asyncio

import pytest

from cssinj.client import Client, Clients

from .conftest import ClientFactory


def test_register_assigns_unique_incrementing_ids(clients: Clients, make_client: ClientFactory) -> None:
    a = clients.register(make_client())
    b = clients.register(make_client())
    c = clients.register(make_client())
    assert (a.id, b.id, c.id) == (1, 2, 3)
    assert len(clients) == 3


def test_get_by_id_accepts_int_and_str(clients: Clients, make_client: ClientFactory) -> None:
    a = clients.register(make_client())
    assert clients.get_by_id(1) is a
    assert clients.get_by_id('1') is a


def test_get_by_id_returns_none_on_missing_or_invalid(clients: Clients, make_client: ClientFactory) -> None:
    clients.register(make_client())
    assert clients.get_by_id(999) is None
    assert clients.get_by_id(None) is None
    assert clients.get_by_id('not-a-number') is None


def test_mutable_sequence_protocol(clients: Clients, make_client: ClientFactory) -> None:
    a = clients.register(make_client())
    b = clients.register(make_client())

    # __getitem__ by index
    assert clients[0] is a
    assert clients[1] is b
    assert clients[:] == [a, b]

    # __contains__
    assert a in clients
    assert make_client() not in clients

    # insert
    c = make_client()
    clients.insert(0, c)
    assert clients[0] is c
    assert clients[1] is a

    # __setitem__ truly replaces (not appends)
    d = make_client()
    clients[0] = d
    assert clients[0] is d
    assert len(clients) == 3

    # __delitem__
    del clients[0]
    assert clients[0] is a


def test_add_returns_new_instance(clients: Clients, make_client: ClientFactory) -> None:
    other = Clients()
    a = clients.register(make_client())
    b = other.register(make_client())
    merged = clients + other
    assert isinstance(merged, Clients)
    assert list(merged) == [a, b]
    # originals untouched
    assert len(clients) == 1
    assert len(other) == 1


def test_add_with_wrong_type_returns_notimplemented(clients: Clients) -> None:
    with pytest.raises(TypeError):
        clients + 42


def test_id_counter_is_per_instance(make_client: ClientFactory) -> None:
    a, b = Clients(), Clients()
    a.register(make_client())
    a.register(make_client())
    b_first = b.register(make_client())
    assert b_first.id == 1, 'second Clients instance must restart its counter'


def test_client_dataclass_defaults() -> None:
    c = Client(host='h', accept=None, headers={}, event=asyncio.Event())
    assert c.id == 0  # only set on register
    assert c.status is True
    assert c.counter == 0
    assert c.data == ''
    assert c.elements == []
