#!/usr/bin/env python3
import sys
import argparse


def main():
    parser = argparse.ArgumentParser(
        prog="CSSINJ.py",
        description="A tool for exfiltrating sensitive information using CSS injection, designed for penetration testing and web application security assessment.",
        epilog="A tool by \33[0;36mAsako\033[0m",
    )
    sub_parser = parser.add_subparsers(title="Category", dest="command", required=True)

    injection_parser = sub_parser.add_parser(
        "inject",
        help="Inject/Exfiltrate data from a website.",
    )
    injection_parser.add_argument(
        "-H", "--hostname", required=True, help="Attacker hostname or IP address"
    )
    injection_parser.add_argument(
        "-p", "--port", required=True, type=int, help="Port number of attacker"
    )
    injection_parser.add_argument(
        "-e",
        "--element",
        required=False,
        help="Specify the HTML element to extract data from",
    )
    injection_parser.add_argument(
        "-a",
        "--attribut",
        required=False,
        help="Specify an element Attribute Selector for exfiltration",
    )
    injection_parser.add_argument(
        "-d",
        "--details",
        action="store_true",
        help="Show detailed logs of the exfiltration process, including extracted data.",
    )
    injection_parser.add_argument(
        "-m",
        "--method",
        default="recursive",
        choices=["recusive", "font-face"],
        help="Specify the type of exfiltration",
    )
    scanner_parser = sub_parser.add_parser(
        "scan",
        help="Check if a website is vulnerable to CSS injection. !!! EXPERIMENTAL !!!!",
    )
    scanner_parser.add_argument(
        "-u",
        "--url",
        required=True,
        help="Specify the target URL to scan for CSS injection vulnerabilities.",
    )
    scanner_parser.add_argument(
        "-d",
        "--delay",
        default="100",
        help="Specify the delay in ms between each request.",
    )
    scanner_parser.add_argument(
        "-c",
        "--crawler",
        action="store_true",
        help="Specify if you want to crawl the website",
    )
    scanner_parser.add_argument(
        "-b", "--cookie", action="append", help="Specify a cookie for request."
    )
    scanner_parser.add_argument(
        "-H", "--headers", action="append", help="Specify an header."
    )
    scanner_parser.add_argument("-U", "--user-agent", help="Specify an User-Agent.")
    # scanner_parser.add_argument(
    #     "--proxy",
    #     action="store_true",
    #     help="If you want to use a proxy."
    # )
    args = parser.parse_args()

    print(
        "\33[1m  _____   _____   _____  _____  _   _       _     _____  __     __\n / ____| / ____| / ____||_   _|| \\ | |     | |   |  __ \\ \\ \\   / /\n| |     | (___  | (___    | |  |  \\| |     | |   | |__) | \\ \\_/ /\n| |      \\___ \\  \\___ \\   | |  | . ` | _   | |   |  ___/   \\   /\n| |____  ____) | ____) | _| |_ | |\\  || |__| | _ | |        | |\n \\_____||_____/ |_____/ |_____||_| \\_| \\____/ (_)|_|        |_|\033[0m\n"
    )
    if args.command == "inject":
        from cssinj.cssinjector import CSSInjector

        CSSInjector().start(args)

    elif args.command == "scan":
        from cssinj.scanner.scanner import Scanner

        scanner = Scanner().start(args)


if __name__ == "__main__":
    main()
    sys.exit(0)
