import re


def is_valid_url(url: str) -> str:
    return re.match(
        r"^https?:\/\/[a-zA-Z0-9-\.]+(?:\:[0-9]+)?(\/[^\s]*)?$",
        url,
    )
