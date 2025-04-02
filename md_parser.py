from enum import StrEnum
from pathlib import Path


class Heading(StrEnum):
    H1 = "# "
    H2 = "## "


class MDParser:
    """Markdown parser to parse my weekly notes and split them into separate files.

    The parser does a single pass to learn the line numbers of H1 and H2 headings.  These can then be queried through property lists.

    The class also provides utility methods for getting the daily date from H1 heading and getting the project name and title of H2 headings.
    """

    def __init__(self, filepath: Path):
        if not filepath.exists():
            raise FileNotFoundError(f"{filepath}")
        with open(filepath, "r") as file:
            data: str = file.read()
            self._lines: list[str] = data.split("\n")

    @property
    def num_lines_parsed(self) -> int:
        return len(self._lines)

    def heading_line_numbers(self, heading: Heading) -> list[int]:
        line_nums: list[int] = []
        for line_num, line in enumerate(self._lines):
            if line.startswith(heading):
                line_nums.append(line_num)
        return line_nums

    def h2_lines_in_h1(self, h1_index: int) -> list[tuple[int, int]]:
        h1_lines: list[int] = self.heading_line_numbers(Heading.H1)
        h2_lines: list[int] = self.heading_line_numbers(Heading.H2)
        return []
