#!/usr/bin/env python3
import sys
import argparse
from cssinj.exfiltrator.cssinjector import CSSInjector


def parse_args():
    parser = argparse.ArgumentParser(
        prog="CSSINJ.py",
        description="A tool for exfiltrating sensitive information using CSS injection, designed for penetration testing and web application security assessment.",
        epilog="A tool by \33[0;36mAsako\033[0m",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-H",
        "--hostname",
        required=True,
        help="Attacker hostname or IP address",
        default="127.0.0.1",
    )
    parser.add_argument(
        "-p",
        "--port",
        required=True,
        type=int,
        help="Port number of attacker",
        default="5005",
    )
    parser.add_argument(
        "-e",
        "--element",
        required=False,
        default="input",
        help="Specify the HTML element to extract data from",
    )
    parser.add_argument(
        "-a",
        "--attribut",
        required=False,
        default="value",
        help="Specify an element Attribute Selector for exfiltration",
    )
    parser.add_argument(
        "-d",
        "--details",
        action="store_true",
        help="Show detailed logs of the exfiltration process, including extracted data.",
    )
    parser.add_argument(
        "-m",
        "--method",
        default="recursive",
        choices=["recusive", "font-face"],
        help="Specify the type of exfiltration",
    )
    parser.add_argument(
        "-o",
        "--output",
        nargs="?",
        const="output.json",
        help="File to store the exfiltrated data in JSON format",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    print(
        "\33[1m  _____   _____   _____  _____  _   _       _     _____  __     __\n / ____| / ____| / ____||_   _|| \\ | |     | |   |  __ \\ \\ \\   / /\n| |     | (___  | (___    | |  |  \\| |     | |   | |__) | \\ \\_/ /\n| |      \\___ \\  \\___ \\   | |  | . ` | _   | |   |  ___/   \\   /\n| |____  ____) | ____) | _| |_ | |\\  || |__| | _ | |        | |\n \\_____||_____/ |_____/ |_____||_| \\_| \\____/ (_)|_|        |_|\033[0m\n"
    )

    CSSInjector().start(args)


if __name__ == "__main__":
    main()
    sys.exit(0)
