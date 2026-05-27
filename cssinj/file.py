import itertools
import json
from pathlib import Path
from typing import NotRequired, TypedDict

from cssinj.client import Client, Clients
from cssinj.utils.dom import Attribute, Element


class ElementDict(TypedDict):
    id: int
    name: str
    attributes: NotRequired[dict[str, str]]


class ClientDict(TypedDict):
    id: int
    headers: dict[str, str]
    elements: list[ElementDict]


class OutputPayload(TypedDict):
    clients: list[ClientDict]


class File:
    def __init__(self, file_name: str) -> None:
        self.base_dir = Path.cwd()
        self.path = self._unique_path(self.base_dir / file_name)

    def _unique_path(self, candidate: Path) -> Path:
        if not candidate.exists():
            return candidate
        stem, suffix = candidate.stem, candidate.suffix
        parent = candidate.parent
        for i in itertools.count(1):
            new_path = parent / f'{stem}{i}{suffix}'
            if not new_path.exists():
                return new_path
        raise RuntimeError('unreachable')  # pragma: no cover

    def write(self, value: str) -> None:
        self.path.write_text(value)


class OutputFile(File):
    def __init__(self, file_name: str, clients: Clients) -> None:
        super().__init__(file_name)
        self.clients = clients

    @staticmethod
    def _attributs_to_dict(attributes: list[Attribute]) -> dict[str, str]:
        return {attribute.name: attribute.value for attribute in attributes}

    @classmethod
    def _element_to_dict(cls, element: Element) -> ElementDict:
        result = ElementDict(id=element.id, name=element.name)
        if element.attributes:
            result['attributes'] = cls._attributs_to_dict(element.attributes)
        return result

    @classmethod
    def _client_to_dict(cls, client: Client) -> ClientDict:
        return {
            'id': client.id,
            'headers': client.headers,
            'elements': [cls._element_to_dict(el) for el in client.elements],
        }

    def update(self) -> None:
        payload: OutputPayload = {'clients': [self._client_to_dict(c) for c in self.clients]}
        self.write(json.dumps(payload, indent=4))
