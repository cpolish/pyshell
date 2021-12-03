"""
A list of reserved symbols that Pyshell can understand

Equivalent to other shell's reserved symbols for features such as:

- directory (current working directory, abbreviated current working directory)
- users (current user)

etc.
"""
import os


# User variables
USER = {
    "{cwd}": "{os.getenv('PWD')}",
    "{user}": "{os.getenv('USER')}",
    "{~}": "{os.getenv('HOME')}",
    "{home}": "{os.getenv('HOME')}"
}

# System variables
SYS = {
    "{host}": "{os.uname()[1]}"
}

VARS = USER | SYS


def interpet_symbols(text: str) -> str:
    for key, val in VARS.items():
        if key in text:
            text = text.replace(key, val)
    f_text = eval(f"f\"{text}\"")
    return f_text
