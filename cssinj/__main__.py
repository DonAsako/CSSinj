#!/usr/bin/env python3
import sys
import argparse
from cssinj.cssinjector import CSSInjector


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
        help="CSS identifier to extract specific data",
    )
    parser.add_argument(
        "-s",
        "--selector",
        help="Specify a CSS Attribute Selector for exfiltration",
        required=False,
    )
    parser.add_argument(
        "-d",
        "--details",
        action="store_true",
        help="Show detailed logs of the exfiltration process, including extracted data.",
    )
    parser.add_argument(
        "-c",
        "--cli",
        action="store_true",
        help="Start an interactive shell (currently unavailable)",
    )
    parser.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="Exfiltrate all available data about the website (currently unavailable)",
    )

    args = parser.parse_args()
    print(
        "\33[1m  _____   _____   _____  _____  _   _       _     _____  __     __\n / ____| / ____| / ____||_   _|| \\ | |     | |   |  __ \\ \\ \\   / /\n| |     | (___  | (___    | |  |  \\| |     | |   | |__) | \\ \\_/ /\n| |      \\___ \\  \\___ \\   | |  | . ` | _   | |   |  ___/   \\   /\n| |____  ____) | ____) | _| |_ | |\\  || |__| | _ | |        | |\n \\_____||_____/ |_____/ |_____||_| \\_| \\____/ (_)|_|        |_|\033[0m\n"
    )

    if args.identifier and args.all or args.selector and args.all:
        print("You can't use -i/--identifier or -s/--selector with -a/--all !")
        sys.exit(1)

    CSSInjector().start(args)


if __name__ == "__main__":
    main()
    sys.exit(0)
