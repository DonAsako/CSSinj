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
        "-c",
        "--cli",
        action="store_true",
        help="Start an interactive shell (currently unavailable)",
    )

    scanner_parser = sub_parser.add_parser(
        "scan",
        help="Check if a website is vulnerable to CSS injection.",
    )
    scanner_parser.add_argument(
        "-u",
        "--url",
        required=True,
        help="Specify the target URL to scan for CSS injection vulnerabilities.",
    )
    args = parser.parse_args()

    print(
        "\33[1m  _____   _____   _____  _____  _   _       _     _____  __     __\n / ____| / ____| / ____||_   _|| \\ | |     | |   |  __ \\ \\ \\   / /\n| |     | (___  | (___    | |  |  \\| |     | |   | |__) | \\ \\_/ /\n| |      \\___ \\  \\___ \\   | |  | . ` | _   | |   |  ___/   \\   /\n| |____  ____) | ____) | _| |_ | |\\  || |__| | _ | |        | |\n \\_____||_____/ |_____/ |_____||_| \\_| \\____/ (_)|_|        |_|\033[0m\n"
    )
    if args.command == "inject":
        from cssinj.cssinjector import CSSInjector
        CSSInjector().start(args)
    elif args.command == "scan":
        from cssinj.scanner import Scanner
        scanner = Scanner()
        try:
            scanner.start(args.url)
        except RuntimeError as e:
            sys.exit(1)
        finally:
            scanner.quit()


if __name__ == "__main__":
    main()
    sys.exit(0)
