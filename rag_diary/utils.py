from pathlib import Path


def guard_file_existence(file_path: Path):
    if not file_path.exists():
        raise FileNotFoundError(file_path)
    if not file_path.is_file():
        raise ValueError(f"{file_path} is not a file")
