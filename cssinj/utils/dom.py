from __future__ import annotations

import dataclasses
import itertools
import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterator

_attribute_ids: Iterator[int] = itertools.count(1)
_element_ids: Iterator[int] = itertools.count(1)


@dataclasses.dataclass
class Attribute:
    name: str
    value: str
    id: int = dataclasses.field(default_factory=lambda: next(_attribute_ids))


@dataclasses.dataclass
class Element:
    name: str
    parent: Element | None = None
    attributes: list[Attribute] = dataclasses.field(default_factory=list)
    children: list[Element] = dataclasses.field(default_factory=list)
    id: int = dataclasses.field(default_factory=lambda: next(_element_ids))
    last_seen: float = dataclasses.field(default_factory=time.time)

    def __post_init__(self) -> None:
        if self.parent is not None:
            self.parent.children.append(self)
