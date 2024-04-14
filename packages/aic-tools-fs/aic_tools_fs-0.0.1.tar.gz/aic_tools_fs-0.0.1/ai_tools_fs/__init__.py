from crewai_tools import tool
from typing import List

import os


@tool("Load list of files in a directory")
def ls(path: str) -> List[str]:
    """Load list of files in a directory."""
    return os.listdir(path)


@tool("Load content of the file, like cat <path>")
def cat(path: str) -> str:
    """Load content of the file, like cat <path>."""
    with open(path, 'r') as f:
        return f.read()
