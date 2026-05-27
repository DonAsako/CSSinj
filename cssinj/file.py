from __future__ import annotations

import itertools
import json
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from cssinj.client import Client, Clients
    from cssinj.utils.dom import Attribut, Element


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
    CLIENT_FIELDS = ('id', 'headers', 'elements')

    def __init__(self, file_name: str, clients: Clients) -> None:
        super().__init__(file_name)
        self.clients = clients

    @staticmethod
    def _attributs_to_dict(attributs: list[Attribut]) -> dict[str, str]:
        return {attribut.name: attribut.value for attribut in attributs}

    @classmethod
    def _element_to_dict(cls, element: Element) -> dict[str, Any]:
        element_dict: dict[str, Any] = {'id': element.id, 'name': element.name}
        if element.attributs:
            element_dict['attributs'] = cls._attributs_to_dict(element.attributs)
        return element_dict

    @classmethod
    def _client_to_dict(cls, client: Client) -> dict[str, Any]:
        return {
            'id': client.id,
            'headers': client.headers,
            'elements': [cls._element_to_dict(el) for el in client.elements],
        }

    def update(self) -> None:
        payload = {'clients': [self._client_to_dict(c) for c in self.clients]}
        self.write(json.dumps(payload, indent=4))
