#!/usr/bin/env python3

import argparse
import os
import pysh_read


def load_rc() -> None:
    pysh_read.interpet(os.environ["PYSHRC"])


def check_rc(file):
    file = os.path.abspath(os.path.expanduser(file))
    err_msg_start = f"error: rc file at '{file}'"
    try:
        open(file, 'r').close()
    except FileNotFoundError:
        raise argparse.ArgumentTypeError(f"{err_msg_start}: does not exist")
    except PermissionError:
        raise argparse.ArgumentTypeError(f"{err_msg_start}: insufficient permissions to open file")
    except OSError as oe:
        raise argparse.ArgumentTypeError(f"{err_msg_start}: cannot open file [Errno {oe.errno}]")
    return file


def prompt() -> None:
    while True:
        user_input = input(os.getenv('PROMPT'))
        print(user_input)


def fetch_args() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", "--rcfile", "-r", nargs=1, default=["~/.pyshrc"], help="specify a custom RC file to use for configuration", type=check_rc)
    args = vars(parser.parse_args())
    os.environ["PYSHRC"] = args["config"][0]


def main() -> None:
    fetch_args()
    load_rc()
    prompt()


if __name__ == "__main__":
    main()
