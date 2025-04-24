from pathlib import Path


def read_file_to_str_list(file: Path) -> list[str]:
    """
    Read a file into a list of strings.
    """
    with open(file, "r") as file:
        data: str = file.read()
        return data.split("\n")
