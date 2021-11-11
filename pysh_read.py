"""
Module which assists with the intepretation of Pyshell scripts and rc files
"""

import sys
from typing import TextIO

def check_mode_python(mode: str) -> bool:
    """
    Checks whether a script should be read respecting Python syntax or traditional shell syntax based on syntax variable in script.

    Returns true if Python specified, false if 'shell', 'bash', etc. specified, and raises an exception for other cases.
    """

    if mode.lower() == "python":
        return True
    elif mode.lower() in {"shell", "sh", "bash"}:
        return False
    else:
        raise TypeError(f"invalid syntax type specified: {mode}")

def split_shell_line(line: str, delim: str, expected_length: int) -> list[str]:
    """Processes a split line to remove extra whitespace and quotes, and returns processed list."""

    raw_split = line.split(delim)
    if len(raw_split) != expected_length:
        raise SyntaxError("invalid split line")
    
    processed_list = []
    for item in raw_split:
        # strip whitespace and quotes
        item = item.strip()
        if item.startswith('"') and item.endswith('"'):
            item = item.strip('"')
        elif item.startswith("'") and item.endswith("'"):
            item = item.strip('"')
        processed_list.append(item)
    
    return processed_list

def python_syntax_enabled(file: TextIO) -> bool:
    """
    Checks whether a syntax variable has been specified in the file, and if so, whether the syntax is Python or not.

    Returns true if Python specified, false if another shell specified.
    """

    for line in file:
        if line.startswith("SYNTAX"):
            split_line = split_shell_line(line, '=', 2)
            break
    
    mode = split_line[1]
    return check_mode_python(mode)

def interpet(filename: str) -> list:
    """
    Main function for interpreting a shell/rc file.

    Returns a list of known parameters.
    """

    using_python_syntax = True
    
    try:
        with open(filename, 'r') as f:
            using_python_syntax = python_syntax_enabled(f)
            f.seek(0)
    except FileNotFoundError:
        print(f"Error: specified file '{filename}' not found", sys.stderr)
    except PermissionError:
        print(f"Error: insufficient permissions for reading from file '{filename}'", sys.stderr)
