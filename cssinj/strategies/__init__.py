from __future__ import annotations

import argparse

from .base import BaseExfiltrationStrategy
from .complete import CompleteStrategy
from .fontface import FontFaceStrategy
from .recursive import RecursiveStrategy

STRATEGIES: dict[str, type[BaseExfiltrationStrategy]] = {
    'recursive': RecursiveStrategy,
    'font-face': FontFaceStrategy,
    'complete': CompleteStrategy,
}


def get_strategy(name: str) -> type[BaseExfiltrationStrategy]:
    if name not in STRATEGIES:
        raise ValueError(f'Unknown strategy: {name}')
    return STRATEGIES[name]


def list_strategies() -> list[str]:
    return list(STRATEGIES.keys())


def build_strategy(args: argparse.Namespace) -> BaseExfiltrationStrategy:
    """Instantiate the strategy selected by CLI args."""
    return get_strategy(args.method)(
        hostname=args.hostname,
        port=args.port,
        element=args.element,
        attribut=args.attribut,
        timeout=args.timeout,
    )


__all__ = [
    'STRATEGIES',
    'BaseExfiltrationStrategy',
    'build_strategy',
    'get_strategy',
    'list_strategies',
]
