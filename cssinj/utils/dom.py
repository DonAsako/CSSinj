import dataclasses
from typing import Optional
from collections.abc import MutableSequence


@dataclasses.dataclass
class Attribut:
    id: int = dataclasses.field(default=0, init=False)
    name: str
    value: str

    _id_counter: int = dataclasses.field(default=0, init=False, repr=False)

    def __post_init__(self):
        self.__class__._id_counter += 1
        self.id = self.__class__._id_counter


@dataclasses.dataclass
class Element:
    id: int = dataclasses.field(default=0, init=False)
    name: str
    parent: Optional["Element"] = None
    attributs: list = dataclasses.field(default_factory=list)
    children: list = dataclasses.field(default_factory=list)
    _id_counter: int = dataclasses.field(default=0, init=False, repr=False)

    def __post_init__(self):
        self.__class__._id_counter += 1
        self.id = self.__class__._id_counter

        # Add element to children list of his parent
        if self.parent:
            self.parent.children.append(self)
