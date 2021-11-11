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
    r"{cwd}": os.getenv("PWD"),
    r"{user}": os.getenv("USER"),
    r"{~}": os.getenv("HOME"),
    r"{home}": os.getenv("HOME")
}

# System variables
SYS = {
    r"{host}": os.getenv("HOST")
}
