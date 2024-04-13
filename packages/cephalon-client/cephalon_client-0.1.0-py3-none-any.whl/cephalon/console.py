import platform
import subprocess
from getpass import getpass
from typing import Optional, Any
from rich.console import Console
from rich.color import ANSI_COLOR_NAMES

c = Console()


def write(
    obj: Any,
    color: Optional[str] = None,
    style: Optional[str] = None,
    pn: bool = False,
    verbose: bool = True,
) -> None:
    """
    verbose print utility with rich formatting

    Args:
        obj (Union[str, Any]): object to print
        color (Optional[str], optional): color of string if string. Defaults to None.
        pn (bool, optional): prepend newline if string. Defaults to False.
        verbose (bool, optional): print object. Defaults to True.

    Raises:
        ValueError: invalid color
    """
    if verbose:
        if isinstance(obj, str):
            if pn:
                obj = f"{obj}"
            if color is None:
                c.print(obj)
            else:
                if color in ANSI_COLOR_NAMES.keys():
                    c.print(f"[{color}]{obj}[/{color}]", style=style)
                else:
                    for acn in ANSI_COLOR_NAMES.keys():
                        c.print(acn, style=style)
                    raise ValueError(
                        f"argument passed to 'color' must be one of the colors listed above"
                    )
        else:
            c.print(obj)


def to_clipboard(text: str) -> None:
    """
    Copies input text to clipboard.

    Args:
        text (str): text to copy to clipboard

    NOTE
    It detects the operating system and uses the appropriate command:

    - pbcopy on MacOS
    - clip on Windows
    - xclip or xsel on Linux

    """
    try:
        os_name = platform.system()
        if os_name == "Darwin":  # MacOS
            process = subprocess.Popen(["pbcopy"], stdin=subprocess.PIPE)
        elif os_name == "Windows":
            process = subprocess.Popen(["clip"], stdin=subprocess.PIPE, shell=True)
        elif os_name == "Linux":
            # Use xclip or xsel, checking which one is installed
            if subprocess.call("command -v xclip", shell=True) == 0:
                process = subprocess.Popen(
                    ["xclip", "-selection", "clipboard"], stdin=subprocess.PIPE
                )
            elif subprocess.call("command -v xsel", shell=True) == 0:
                process = subprocess.Popen(
                    ["xsel", "--clipboard", "--input"], stdin=subprocess.PIPE
                )
            else:
                print("No suitable clipboard utility found on your system.")
                return
        else:
            raise OSError("Unsupported OS")
        process.communicate(text.encode("utf-8"))
    except Exception as e:
        raise e


def visible_input(message: str, color: str = "dark_orange", icon: str = "➜"):
    write(f"{message}", color=color)
    user_input = str(input(f"{icon} "))
    return user_input


def secure_input(message: str, color: str = "dark_orange", icon: str = "🔑"):
    write(f"[{color}]{message}[/{color}]")
    user_input = getpass(f"{icon} ")
    return user_input
