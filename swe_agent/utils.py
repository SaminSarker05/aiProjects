from langchain_core.tools import tool  # define tools for AI agent
import pathlib
from typing import Tuple

ROOT = pathlib.Path.cwd() / "monkey-generated-code"

def check_safety(path: str) -> pathlib.Path:
    p = (ROOT / path).resolve()
    if ROOT.resolve() not in p.parents and ROOT.resolve() != p.parent and ROOT.resolve() != p:
        raise Exception(f"File is not in safe directory: {p}")
    return p

@tool
def write_file(path: str, content: str) -> str:
    """
    write content to specified file path within project root.
    """
    path = check_safety(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return f"File {path} written."

@tool
def read_file(path: str) -> str:
    """
    read content from specified file path within project root.
    """
    path = check_safety(path)
    if not path.exists():
        return "File does not exist."
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

@tool
def get_cwd() -> str:
    """
    get current working directory.
    """
    return str(ROOT)

@tool
def ls_files(directory: str = ".") -> str:
    """
    list files in specified directory.
    """
    path = check_safety(directory)
    if not path.is_dir():
        return "Not a directory."
    # get all files in directory recursively
    files = [str(f.relative_to(ROOT)) for f in path.glob("**/*") if f.is_file()]
    return "\n".join(files) if files else "No files found."

@tool
def run_cmd(cmd: str, cwd: str = None, timeout: int = 25) -> Tuple[int, str, str]:
    """
    run given command in specified directory.
    """
    cwd_dir = check_safety(cwd) if cwd else ROOT
    res = subprocess.run(
        cmd, shell=True, capture_output=True, cwd=str(cwd_dir), timeout=timeout, text=True
    )
    return res.returncode, res.stdout, res.stderr

@tool
def list_tools():
    """
    list all available tools.
    """
    return "write_file, read_file, get_cwd, ls_files, run_cmd"

def init_root():
    ROOT.mkdir(parents=True, exist_ok=True)
    return str(ROOT)
