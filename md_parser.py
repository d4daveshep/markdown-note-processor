import re
from enum import StrEnum
from pathlib import Path
from typing import NamedTuple


class Heading(StrEnum):
    H1 = "# "
    H2 = "## "


class LineRange(NamedTuple):
    start: int
    end: int


class H2_Heading(NamedTuple):
    lines: LineRange
    project_name: str
    title: str = ""


class H1_Heading(NamedTuple):
    line_num: int
    date: str
    h2s: list[H2_Heading]


class NoteFileStructure(NamedTuple):
    line_count: int
    h1_headings: list[H1_Heading]


class NoteFile:
    """
    Note file parser to parse my weekly notes and split them into separate files.

    The file is parsed to create a NoteFileStructure object which contains the structure of the file.
    """

    def __init__(self, filepath: Path):
        if not filepath.exists():
            raise FileNotFoundError(f"{filepath}")
        with open(filepath, "r") as file:
            data: str = file.read()
            self._lines: list[str] = data.split("\n")

    @staticmethod
    def validate_weekly_heading(heading: str) -> bool:
        pattern: str = r"^# W(0[1-9]|[1-4][0-9]|5[0-2])\s+\d{4}:"

        return bool(re.match(pattern, heading))

    def analyse_structure(self) -> NoteFileStructure:
        """
        start at the top of the file
        we're not in an H1 or H2
        if we hit H1, save line as H1.start and remember we're in an H1
        if we hit H2 before H1 then raise an error and stop
        if we hit H2 after H1 then save line as H2 start and remember we're in an H2
        if we hit H1 while in H1 then save line-1 as H1 end and H2 end
        """

        file_structure: NoteFileStructure = NoteFileStructure(
            line_count=len(self._lines), h1_headings=None
        )
        return file_structure

    def split_file(self, file_structure: NoteFileStructure) -> None:
        pass

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
