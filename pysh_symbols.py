"""
A list of reserved symbols that Pyshell can understand

Equivalent to other shell's reserved symbols for features such as:

- directory (current working directory, abbreviated current working directory)
- users (current user)

etc.
"""
import os
from typing import Callable


# User variables
USER = {
    "{cwd}": "{PWD}",
    "{user}": "{USER}",
    "{~}": "{HOME}",
    "{home}": "{HOME}"
}

# System variables
SYS = {
    "{host}": "{HOST}"
}

VARS = USER | SYS


def interpet_symbols(text: str) -> str:
    for key, val in VARS.items():
        if key in text:
            text = text.replace(key, val)
    return text
