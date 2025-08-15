import os
import json
from pathlib import Path


class File:
    def __init__(self, file_name):
        self.base_dir = Path.cwd()
        self.file_name = self.generate_file_name(file_name)
        self.create_file()

    def generate_file_name(self, file_name):
        i = 0
        new_file_name = file_name
        while os.path.exists(self.base_dir / new_file_name):
            i += 1
            new_file_name = file_name + str(i)
        return new_file_name

    def create_file(self):
        with open(self.base_dir / self.file_name, "w") as f:
            pass

    def update_file(self, value):
        with open(self.base_dir / self.file_name, "w") as f:
            f.write(value)


class OutputFile(File):
    def __init__(self, file_name, clients):
        super().__init__(file_name)
        self.clients = clients
        self.client_fields = ["id", "headers", "elements"]

    def attributs_to_dict(self, attributs):
        attributs_dict = {}
        for attribut in attributs:
            attributs_dict[attribut.name] = attribut.value
        return attributs_dict

    def element_to_dict(self, element):
        element_dict = {
            "id": element.id,
            "name": element.name,
        }
        if element.attributs:
            element_dict["attributs"] = self.attributs_to_dict(element.attributs)

        return element_dict

    def client_to_dict(self, client):
        client_dict = {
            field: getattr(client, field)
            for field in self.client_fields
            if field != "elements"
        }
        client_dict["elements"] = [self.element_to_dict(el) for el in client.elements]
        return client_dict

    def update(self):
        clients_list = {
            "clients": [self.client_to_dict(client) for client in self.clients]
        }
        self.update_file(json.dumps(clients_list, indent=4))
