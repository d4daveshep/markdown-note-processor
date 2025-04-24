from pathlib import Path
from md_parser import Heading


def read_file_to_str_list(file: Path) -> list[str]:
    """
    Read a file into a list of strings.
    """
    with open(file, "r") as file:
        data: str = file.read()
        return data.split("\n")


def get_h2_headings(file: Path) -> set[str]:
    """
    Filter the H2 headings out of the file and return them as a set
    """
    lines: list[str] = read_file_to_str_list(file)

    return {line for line in lines if line.startswith(Heading.H2)}
