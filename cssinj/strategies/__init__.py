from .fontface import FontFaceStrategy
from .recursive import RecursiveStrategy

STRATEGIES = {
    "recursive": RecursiveStrategy,
    "font-face": FontFaceStrategy,
}


def get_strategy(name: str):
    if name not in STRATEGIES:
        raise ValueError(f"Unknown strategy: {name}")
    return STRATEGIES[name]


def list_strategies() -> list[str]:
    return list(STRATEGIES.keys())


__all__ = [
    "get_strategy",
    "list_strategies",
]
