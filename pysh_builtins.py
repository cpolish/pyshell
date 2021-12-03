"""Module specifying shell builtins for Pyshell"""
import os
import re


BUILTINS = {
    "cd": 1,
    "echo": -1
}


def run_builtin(cmd: str, args: tuple[str, ...]) -> None:
    if (BUILTINS[cmd] != -1) and (len(args) != BUILTINS[cmd]):
        raise IndexError(f"not enough arguments for command {cmd}")
    
    if cmd == "cd":
        new_dir = args[0]
        if os.path.isfile(new_dir):
            print(f"cd: {new_dir}: is a file")
        else:
            os.environ["PWD"] = os.path.abspath(new_dir)
            os.chdir(new_dir)
    elif cmd == "echo":
        args_with_vars = (os.path.expandvars(arg) if re.match(r"^\$.", arg) else arg for arg in args)
        print(*args_with_vars)
