from pathlib import Path


def relative_to_cwd(path_str: str):
    path = Path(path_str)
    if path.is_relative_to(Path.cwd()):
        path = path.relative_to(Path.cwd())
    return path
