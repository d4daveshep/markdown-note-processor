import logging
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from io import TextIOWrapper
from pathlib import Path

import structlog

log: structlog.BoundLogger = structlog.get_logger()
structlog.configure(wrapper_class=structlog.make_filtering_bound_logger(logging.DEBUG))


class FormatException(Exception):
    pass


@dataclass
class NoteSummary:
    title: str
    date_str: str
    lines_written: int = 0


@dataclass
class ProjectFileDetails:
    name: str
    date_str: str = ""
    created: bool = False
    entries: list[NoteSummary] = field(default_factory=list)


@dataclass
class SplitResults:
    lines_procesed: int = 0
    week_num: str = ""
    projects: dict[str, ProjectFileDetails] = field(default_factory=dict)
    days: set[str] = field(default_factory=set)


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
        self.file_directory: Path = filepath.parent
        with open(filepath, "r") as file:
            data: str = file.read()
            self._lines: list[str] = data.split("\n")

        NoteFile.validate_weekly_heading(self._lines[0])

    def split_file(self) -> SplitResults:
        """
        Split the file based on the Parsing Rules.md file

        Return the summary results in a SplitResults object
        """
        results: SplitResults = SplitResults(lines_procesed=0)
        date_str: str = ""
        project_name: str = ""
        title: str = ""
        week_num: str = ""
        project_file: TextIOWrapper = open("/dev/null")

        log.debug("START")

        # loop through the lines, use 1-based line numbering to ease debugging and output
        for line_num, line in enumerate(self._lines, start=1):
            # process the first line separately as it contains the week number we need
            if line_num == 1:
                log.debug(f"line {line_num}: H1 Week heading")
                week_num = NoteFile.validate_weekly_heading(line)
                results.week_num = week_num

            elif line.startswith(Heading.H1):
                log.debug(f"line {line_num}: H1 heading: {line[2:]}")
                date_str = NoteFile.validate_date_heading(h1_heading=line)

                # close the project file (if it's open)
                project_name = ""
                project_file.close()

            elif line.startswith(Heading.H2):
                log.debug(f"line {line_num}: H2 heading: {line[3:]}")

                project_name, title = NoteFile.split_project_name_heading(line)
                project_details: ProjectFileDetails = ProjectFileDetails(
                    name=project_name
                )

                # close the previous project file and open/create the new one for appending text
                project_file.close()
                # if the file already exists then just open it, otherwise create it and write the project name as a H1 heading
                if (self.file_directory / Path(project_name + ".md")).exists():
                    project_file = open(
                        self.file_directory / Path(project_name + ".md"), "a"
                    )
                    project_details.created = False
                else:
                    project_file = open(
                        self.file_directory / Path(project_name + ".md"), "a"
                    )
                    project_file.write(f"# {project_name}\n\n")
                    project_details.created = True
                results.projects[project_name] = project_details

                # if use the week_num if we don't have a date_str
                if date_str == "":
                    project_file.write(f"## {week_num}: {title}\n")
                    project_details.entries.append(
                        NoteSummary(title=title, date_str=week_num)
                    )
                else:
                    project_file.write(f"## {date_str}: {title}\n")
                    project_details.entries.append(
                        NoteSummary(title=title, date_str=week_num)
                    )

            elif project_name:
                log.debug(f"line {line_num}: Appending to project: {project_name}")
                project_file.write(line + "\n")
                assert False, "TODO really need to refactor and sort out the logic"
                note_summary: NoteSummary = results.projects[project_name].entries[
                    (title, date_str)
                ]
                note_summary.lines_written += 1

            else:
                # write the line to the project file or ignore it
                log.debug(f"line {line_num}: IGNORED")

            results.lines_procesed += 1

        project_file.close()
        return results

    @property
    def num_lines_parsed(self) -> int:
        return len(self._lines)

    @staticmethod
    def validate_weekly_heading(h1_heading: str) -> str:
        """
        Validate the heading matches the correct weekly format: # Week nn yyyy: <date range>

        Rules are as follows:
            nn must be two digits e.g. 01, 45
            yyyy is the year
            <date range> is not validated and could be any text

        Return: the week string e.g. "Week 12 2024"
        """
        pattern: str = r"^# Week\s(0[1-9]|[1-4][0-9]|5[0-2])\s+\d{4}:"

        if bool(re.match(pattern, h1_heading)):
            log.debug(f'Week_num="{h1_heading[2:14]}"')
            return h1_heading[2:14]
        else:
            raise FormatException(
                'Invalid format on line 1, expecting "# Week nn yyyy: ..."'
            )

    @staticmethod
    def split_project_name_heading(h2_heading: str) -> tuple[str, str]:
        """
        Split the H2 heading into project name and title around the first hyphen in the heading

        Return: project_name, title
        """
        project_name: str
        title: str
        if not h2_heading.startswith("## ") or len(h2_heading) < 4:
            raise FormatException('Invalid format, expecting "## <project name>"')
        hyphen_index: int = h2_heading.find("-", 3)
        if hyphen_index == -1:
            project_name = h2_heading[3:]
            title = ""
        else:
            project_name = h2_heading[3:hyphen_index]
            title = h2_heading[hyphen_index + 1 :]
        if project_name == "":
            raise FormatException('Invalid format, expecting "# <project name>"')
        log.debug(f'Project_name="{project_name}", Title="{title}"')
        return project_name.strip(), title.strip()

    @staticmethod
    def validate_date_heading(h1_heading: str) -> str:
        """
        Validate the H1 heading is a valid date in the format Mon 6 Jan 2025.
        Raise: FormatException if format is invalid, note the day of week is not verified to be correct
        Return: the date in same format it was specified
        """
        if not h1_heading.startswith("# ") or len(h1_heading) < 3:
            raise FormatException('Invalid date format, expecting "# ddd dd mmm yyyy"')
        date_str: str = h1_heading[2:]
        try:
            datetime.strptime(date_str, "%a %d %b %Y")
            log.debug(f'Date_str="{date_str}"')
        except ValueError:
            log.debug(
                f'Invalid date format: "{h1_heading}" - Ignoring lines until valid date found'
            )
            date_str = ""
        return date_str


if __name__ == "__main__":
    if len(sys.argv) > 1:
        note_filepath: str = sys.argv[1]

        weekly_notefile: NoteFile = NoteFile(Path(note_filepath))
        results: SplitResults = weekly_notefile.split_file()
        print("\nCompleted\n")
        print(results)
