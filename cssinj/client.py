from collections.abc import MutableSequence
import dataclasses
import asyncio
import time


@dataclasses.dataclass
class Client:
    id: int = dataclasses.field(default=0, init=False)
    host: str
    headers: dict
    accept: str
    status: bool = dataclasses.field(default=True, init=False)
    counter: int = dataclasses.field(default=0, init=False)
    event: asyncio.Event
    elements: list = dataclasses.field(default_factory=list)
    data: str = dataclasses.field(default_factory=str, init=False)
    _id_counter: int = dataclasses.field(default=0, init=False, repr=False)

    def __post_init__(self):
        self.__class__._id_counter += 1
        self.id = self.__class__._id_counter


class Clients(MutableSequence):
    def __init__(self):
        super().__init__()
        self.client_list = []

    def __repr__(self):
        return f"<{self.__class__.__name__} clients: {repr(self.client_list)}>"

    def __contains__(self, value):
        return value in self.client_list

    def __len__(self):
        return len(self.client_list)

    def __getitem__(self, id):
        client = self.get_client_by_id(id)
        return client

    def __delitem__(self, id):
        item = self.get_client_by_id(id)
        self.client_list.remove(item)
        return item

    def __setitem__(self, i, client):
        self.client_list.append(client)

    def __iter__(self):
        return iter(self.client_list)

    def append(self, client):
        self.client_list.append(client)

    def insert(self, id, new_client):
        for i in range(len(self.client_list)):
            if self.client_list[i].id == id:
                self.client_list[i] = new_client

    def __add__(self, another_clients):
        if isinstance(another_clients, Clients):
            return self.__class__(self.client_list + another_clients)

    def get_client_by_id(self, id):
        for client in self.client_list:
            if client.id == int(id):
                return client

    def clear(self):
        self.client_list.clear()
