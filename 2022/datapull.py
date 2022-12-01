import argparse
import datetime
import os
import urllib.error
import urllib.request
from typing import Optional
from typing import Sequence


def _ensure_token() -> None:
    """Create the session token file."""

    if os.path.exists(".token"):
        return

    print("A session token is required to use this tool.")
    print("Please visit https://adventofcode.com/ and log in.")
    print("Next, copy the value of the session cookie from your browser.")
    print("Paste it below:")
    token = input("> ")
    with open(".token", "w") as file:
        file.write(token)


def _read_cookie() -> str:
    """Read the session token from the .env file."""
    with open(".token", "r") as file:
        return file.read().strip()


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--day", type=int, help="The day")
    parser.add_argument("-y", "--year", type=int, help="The year")
    args = parser.parse_args(argv)

    _ensure_token()
    cookie = _read_cookie()

    if args.day is None and args.year is None:
        today = datetime.date.today()
        args.day = today.day
        args.year = today.year

    # get request to url
    url = f"https://adventofcode.com/{args.year}/day/{args.day}/input"

    print(args, url)

    request = urllib.request.Request(url)
    request.add_header("Cookie", f"session={cookie}")

    try:
        with urllib.request.urlopen(request) as response:
            data = response.read().decode("utf-8")
    except urllib.error.HTTPError:
        print("Day not ready yet!")
        return 1

    with open("input.txt", "w") as file:
        file.write(data)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
