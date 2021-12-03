#!/usr/bin/env python3

import argparse
import os
import pysh_builtins
import pysh_read
import shlex
import subprocess
import sys


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


def get_user_input() -> tuple[str, ...]:
    prompt = os.getenv("PROMPT").format(**os.environ)
    user_input = input(prompt)
    user_input_split = shlex.split(user_input)
    return tuple(user_input_split)


def prompt() -> None:
    while True:
        try:
            user_input_split = get_user_input()
            user_input_cmd = user_input_split[0]
            if user_input_cmd == "exit":
                break
            elif user_input_cmd in pysh_builtins.BUILTINS:
                pysh_builtins.run_builtin(user_input_cmd, user_input_split[1:])
            else:
                subprocess.run(user_input_split)
        except (EOFError, KeyboardInterrupt):
            print()
        except FileNotFoundError:
            print(f"pysh: unknown command: {user_input_split[0]}", file=sys.stderr)


def setup_env_vars() -> None:
    os.environ["HOST"] = os.uname()[1]


def fetch_args() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", "--rcfile", "-r", nargs=1, default=["~/.pyshrc"], help="specify a custom RC file to use for configuration", type=check_rc)
    args = vars(parser.parse_args())
    os.environ["PYSHRC"] = args["config"][0]


def main() -> None:
    fetch_args()
    setup_env_vars()
    load_rc()
    prompt()


if __name__ == "__main__":
    main()
