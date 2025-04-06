import logging
import re
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from pathlib import Path

import structlog

log: structlog.BoundLogger = structlog.get_logger()
structlog.configure(wrapper_class=structlog.make_filtering_bound_logger(logging.DEBUG))


class FormatException(Exception):
    pass


@dataclass
class SplitResults:
    lines_procesed: int


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

    @staticmethod
    def split_project_name_heading(heading: str) -> tuple[str, str]:
        """
        Split the heading into project name and title around the first hyphen in the heading

        Return: project_name, title
        """
        project_name: str
        title: str
        if not heading.startswith("# ") or len(heading) < 3:
            raise FormatException('Invalid format, expecting "# <project name>"')
        hyphen_index: int = heading.find("-", 2)
        if hyphen_index == -1:
            project_name = heading[2:]
            title = ""
        else:
            project_name = heading[2:hyphen_index]
            title = heading[hyphen_index + 1 :]
        if project_name == "":
            raise FormatException('Invalid format, expecting "# <project name>"')
        log.debug(f'Project_name="{project_name}", Title="{title}"')
        return project_name.strip(), title.strip()

    @staticmethod
    def validate_date_heading(h1_heading: str) -> str:
        """
        Validate the H1 heading is a valid date in the format Mon 6 Jan 2025.
        Raise FormatException if format is invalid
        Return: the date in same format it was specified
        """
        if not h1_heading.startswith("# ") or len(h1_heading) < 3:
            raise FormatException('Invalid date format, expecting "# ddd dd mmm yyyy"')
        date_str: str = h1_heading[2:]
        try:
            datetime.strptime(date_str, "%a %d %b %Y")
        except ValueError:
            raise FormatException('Invalid date format, expecting "# ddd dd mmm yyyy"')
        return date_str

    def split_file(self) -> SplitResults:
        results: SplitResults = SplitResults(lines_procesed=0)
        for line_num, line in enumerate(self._lines, start=1):
            if line.startswith(Heading.H1):
                log.debug(f"line {line_num}: H1 heading: {line[2:]}")
                project_name, title = NoteFile.split_project_name_heading(line)
                assert False, "TODO do something with project name and title"
        return results

    @property
    def num_lines_parsed(self) -> int:
        return len(self._lines)
