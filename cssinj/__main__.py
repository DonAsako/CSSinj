#!/usr/bin/env python3
import sys
import argparse
from cssinj.CSSINJ import CssInjector


def main():
    parser = argparse.ArgumentParser(
        prog="CSSINJ.py",
        description="A tool for exfiltrating sensitive information using CSS injection, designed for penetration testing and web application security assessment.",
        epilog="A tool by \33[0;36mAsako\033[0m",
    )
    parser.add_argument(
        "-H", "--hostname", required=True, help="Attacker hostname or IP address"
    )
    parser.add_argument(
        "-p", "--port", required=True, type=int, help="Port number of attacker"
    )
    parser.add_argument(
        "-i",
        "--identifier",
        required=False,
        default="all",
        help="CSS identifier to extract specific data",
    )
    parser.add_argument(
        "-s",
        "--selector",
        help="Specify a CSS Attribute Selector for exfiltration",
        default="value",
        required=False,
    )
    parser.add_argument(
        "-d",
        "--details",
        action="store_true",
        help="Show detailed logs of the exfiltration process, including extracted data.",
    )
    args = parser.parse_args()

    print(
        "\33[1m  _____   _____   _____  _____  _   _       _     _____  __     __\n / ____| / ____| / ____||_   _|| \\ | |     | |   |  __ \\ \\ \\   / /\n| |     | (___  | (___    | |  |  \\| |     | |   | |__) | \\ \\_/ /\n| |      \\___ \\  \\___ \\   | |  | . ` | _   | |   |  ___/   \\   /\n| |____  ____) | ____) | _| |_ | |\\  || |__| | _ | |        | |\n \\_____||_____/ |_____/ |_____||_| \\_| \\____/ (_)|_|        |_|\033[0m\n"
    )

    CssInjector().start(args)


if __name__ == "__main__":
    main()
    sys.exit(0)
