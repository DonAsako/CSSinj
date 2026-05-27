from __future__ import annotations

import asyncio
import dataclasses
import itertools
from collections.abc import Iterable, Iterator, MutableSequence
from typing import overload

from cssinj.utils.dom import Element


@dataclasses.dataclass
class Client:
    host: str
    headers: dict[str, str]
    accept: str | None
    event: asyncio.Event
    id: int = dataclasses.field(default=0)
    status: bool = dataclasses.field(default=True)
    counter: int = dataclasses.field(default=0)
    elements: list[Element] = dataclasses.field(default_factory=list)
    data: str = dataclasses.field(default='')


class Clients(MutableSequence[Client]):
    def __init__(self) -> None:
        self._items: list[Client] = []
        self._id_counter: Iterator[int] = itertools.count(1)

    def __repr__(self) -> str:
        return f'<{type(self).__name__} clients: {self._items!r}>'

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self) -> Iterator[Client]:
        return iter(self._items)

    def __contains__(self, value: object) -> bool:
        return value in self._items

    @overload
    def __getitem__(self, index: int) -> Client: ...
    @overload
    def __getitem__(self, index: slice) -> list[Client]: ...
    def __getitem__(self, index: int | slice) -> Client | list[Client]:
        return self._items[index]

    @overload
    def __setitem__(self, index: int, value: Client) -> None: ...
    @overload
    def __setitem__(self, index: slice, value: Iterable[Client]) -> None: ...
    def __setitem__(self, index, value) -> None:  # type: ignore[no-untyped-def]
        self._items[index] = value

    def __delitem__(self, index: int | slice) -> None:
        del self._items[index]

    def insert(self, index: int, value: Client) -> None:
        self._items.insert(index, value)

    def __add__(self, other: object) -> Clients:
        if not isinstance(other, Clients):
            return NotImplemented  # type: ignore[return-value]
        merged = Clients()
        merged._items = self._items + other._items
        return merged

    def register(self, client: Client) -> Client:
        """Assign a unique id and append the client."""
        client.id = next(self._id_counter)
        self._items.append(client)
        return client

    def get_by_id(self, client_id: int | str | None) -> Client | None:
        if client_id is None:
            return None
        try:
            target = int(client_id)
        except (TypeError, ValueError):
            return None
        for client in self._items:
            if client.id == target:
                return client
        return None
