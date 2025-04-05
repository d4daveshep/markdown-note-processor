import re
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

# class LineRange(NamedTuple):
#     start: int
#     end: int
#
#
# class H2_Heading(NamedTuple):
#     lines: LineRange
#     project_name: str
#     title: str = ""
#
#
# class H1_Heading(NamedTuple):
#     line_num: int
#     date: str
#     h2s: list[H2_Heading]
#
#
# class NoteFileStructure(NamedTuple):
#     line_count: int
#     h1_headings: list[H1_Heading]


class FormatException(Exception):
    pass


@dataclass
class SplitResults:
    lines_procesed: int = 0


class Heading(StrEnum):
    H1 = "# "
    H2 = "## "


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

        NoteFile.validate_weekly_heading(self._lines[0])

    @staticmethod
    def validate_weekly_heading(heading: str) -> bool:
        """
        Validate the heading matches the correct weekly format: # Wnn yyyy: <date range>

        Rules are as follows:
            Wnn must be two digits e.g. 01, 45
            yyyy is the year
            <date range> is not validated and could be any text
        """
        pattern: str = r"^# W(0[1-9]|[1-4][0-9]|5[0-2])\s+\d{4}:"

        if bool(re.match(pattern, heading)):
            return True
        else:
            raise FormatException(
                'Invalid format on line 1, expecting "# Wnn yyyy: ..."'
            )

    def split_file(self) -> SplitResults:
        return SplitResults()

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
