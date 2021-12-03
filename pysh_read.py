"""
Module which assists with the intepretation of Pyshell scripts and rc files
"""
import importlib.util
import os
import pysh_symbols
import re
import subprocess
import sys
from typing import Any, TextIO


REQUIRED_IMPORTS = """\
import os
import sys


"""

RC_FILENAMES = {".pyshrc"}

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


def write_tmp_script(path: str, f_str: str) -> str:
    f_name = path.split('/')[-1]
    tmp_path = "/tmp/" + f_name + ".py"
    with open(tmp_path, 'w') as tmp_f:
        tmp_f.write(REQUIRED_IMPORTS)
        tmp_f.write(f_str)
    
    return tmp_path


def read_python_script(filename: str) -> str:
    with open(filename, 'r') as f:
        while True:
            if f.readline().startswith("SYNTAX"):
                f.readline()
                break
            f.readline()
        
        f_str = f.read()
    return f_str


def set_rc_env_vars(module_vars: dict[str, Any]) -> None:
    for var_name, var_val in module_vars.items():
        if re.match("{[^}]*}", var_val):
            var_val = pysh_symbols.interpet_symbols(var_val)
        
        os.environ[var_name] = var_val


def read_rc_file(filename: str) -> None:
    module_name = filename.removesuffix(".py")
    spec = importlib.util.spec_from_file_location(module_name, filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    variables = {var_name for var_name in vars(module) if not var_name.startswith("__")}
    module_vars = {k: v for k, v in vars(module).items() if (k in variables) and isinstance(v, (str, int, float, bool, list, tuple, dict, set))}
    set_rc_env_vars(module_vars)


def construct_python_script(filename: str) -> str:
    script_str = read_python_script(filename)
    tmp_path = write_tmp_script(filename, script_str)
    return tmp_path


def interpet(filename: str) -> None:
    """Main function for interpreting a shell/rc file."""
    using_python_syntax = True
    try:
        with open(filename, 'r') as f:
            using_python_syntax = python_syntax_enabled(f)
            f.seek(0)
    except FileNotFoundError:
        print(f"Error: specified file '{filename}' not found", sys.stderr)
    except PermissionError:
        print(f"Error: insufficient permissions for reading from file '{filename}'", sys.stderr)
    
    if using_python_syntax:
        tmp_path = construct_python_script(filename)
        if filename.split('/')[-1] in RC_FILENAMES:
            read_rc_file(tmp_path)
        else:
            subprocess.run("python3", tmp_path)
    else:
        subprocess.run(["sh", filename])
