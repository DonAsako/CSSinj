import dataclasses
from typing import Optional


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
    parent: Optional["Element"]
    attributs: list = dataclasses.field(default_factory=list)
    children: list = dataclasses.field(default_factory=list)
    _id_counter: int = dataclasses.field(default=0, init=False, repr=False)

    def __post_init__(self):
        self.__class__._id_counter += 1
        self.id = self.__class__._id_counter

        # Add element to children list of his parent
        if self.parent:
            self.parent.children.append(self)

class Elements(MutableSequence):
    def __init__(self):
        super().__init__()
        self.element_list = []

    def __repr__(self):
        return f"<{self.__class__.__name__} elements: {repr(self.element_list)}>"

    def __contains__(self, value):
        return value in self.element_list

    def __len__(self):
        return len(self.element_list)

    def __getitem__(self, id):
        element = self.get_elemnt_by_id(id)
        return element

    def __delitem__(self, id):
        item = self.get_element_by_id(id)
        self.element_list.remove(item)
        return item

    def __setitem__(self, i, element):
        self.element_list.append(element)

    def append(self, element):
        self.element_list.append(element)

    def insert(self, id, new_element):
        for i in range(len(self.element_list)):
            if self.element_list[i].id == id:
                self.element_list[i] = new_element

    def __add__(self, another_elements):
        if isinstance(another_elements, elements):
            return self.__class__(self.element_list + another_elements)

    def get_element_by_id(self, id):
        for element in self.element_list:
            if element.id == int(id):
                return element

    def clear(self):
        self.element_list.clear()
