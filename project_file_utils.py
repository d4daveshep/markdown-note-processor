from pathlib import Path
from enum import StrEnum


class Heading(StrEnum):
    H1 = "# "
    H2 = "## "


def read_file_to_str_list(filepath: Path) -> list[str]:
    """
    Read a file into a list of strings.
    """
    with open(filepath, "r") as file:
        data: str = file.read()
        return data.split("\n")


def get_h2_headings(file: Path) -> set[str]:
    """
    Filter the H2 headings out of the file and return them as a set
    """
    lines: list[str] = read_file_to_str_list(file)

    return {line for line in lines if line.startswith(Heading.H2)}


class ProjectFileHeadings:
    def __init__(self, directory: Path) -> None:
        self._cache: dict[str, set[str]] = {}
        self.directory = directory
        self.read_project_files(directory)

    def read_project_files(self, directory: Path) -> int:
        self._cache = {}
        for md_file in directory.glob("*.md"):
            self._cache[md_file.stem] = get_h2_headings(md_file)
        return len(self._cache)

    def contains(self, project_filename: str, h2_heading: str) -> bool:
        try:
            return h2_heading in self._cache[project_filename]
        except KeyError:
            return False
