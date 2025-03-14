from dataclasses import dataclass

@dataclass
class Client:
    id: int
    host: str
    user_agent: str
    accept: str
    elements = []
