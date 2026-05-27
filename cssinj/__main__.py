import argparse
import sys
from pathlib import Path

from cssinj.console import setup_logging
from cssinj.exfiltrator.cssinjector import CSSInjector
from cssinj.strategies import list_strategies

BANNER = """
\33[1m  _____   _____   _____  _____  _   _       _     _____  __     __
 / ____| / ____| / ____||_   _|| \\ | |     | |   |  __ \\ \\ \\   / /
| |     | (___  | (___    | |  |  \\| |     | |   | |__) | \\ \\_/ /
| |      \\___ \\  \\___ \\   | |  | . ` | _   | |   |  ___/   \\   /
| |____  ____) | ____) | _| |_ | |\\  || |__| | _ | |        | |
 \\_____||_____/ |_____/ |_____||_| \\_| \\____/ (_)|_|        |_|\033[0m
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog='CSSINJ.py',
        description=(
            'A tool for exfiltrating sensitive information using CSS injection, '
            'designed for penetration testing and web application security assessment.'
        ),
        epilog='A tool by \33[0;36mDonAsako\033[0m',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        '-H',
        '--hostname',
        default='127.0.0.1',
        help='Attacker hostname or IP address',
    )
    parser.add_argument(
        '-p',
        '--port',
        type=int,
        default=5005,
        help='Port number of attacker',
    )
    parser.add_argument(
        '-e',
        '--element',
        required=False,
        default='input',
        help='Specify the HTML element to extract data from',
    )
    parser.add_argument(
        '-a',
        '--attribute',
        '--attribut',  # deprecated alias
        dest='attribute',
        default='value',
        help='Specify an element Attribute Selector for exfiltration',
    )
    parser.add_argument(
        '-d',
        '--details',
        action='store_true',
        help='Show detailed logs of the exfiltration process, including extracted data.',
    )
    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        help='Enable debug-level logging.',
    )
    verbosity.add_argument(
        '-q',
        '--quiet',
        action='store_true',
        help='Only log warnings and errors.',
    )
    parser.add_argument(
        '--no-banner',
        action='store_true',
        help='Do not print the ASCII banner on startup.',
    )
    parser.add_argument(
        '--log-file',
        type=Path,
        default=None,
        help='Also write structured logs to this file.',
    )
    parser.add_argument(
        '-m',
        '--method',
        default='recursive',
        choices=list_strategies(),
        help='Specify the type of exfiltration',
    )
    parser.add_argument(
        '-o',
        '--output',
        nargs='?',
        const='output.json',
        help='File to store the exfiltrated data in JSON format',
    )
    parser.add_argument(
        '-t',
        '--timeout',
        type=float,
        default=3.0,
        help='Timeout in seconds before considering exfiltration complete (useful for font-face)',
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.no_banner:
        sys.stdout.write(BANNER + '\n')
    setup_logging(
        quiet=args.quiet,
        verbose=args.verbose or args.details,
        log_file=args.log_file,
    )
    CSSInjector().start(args)


if __name__ == '__main__':
    main()
    sys.exit(0)
