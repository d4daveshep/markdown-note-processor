import argparse
import logging
import re
from dataclasses import dataclass
from datetime import datetime
from io import TextIOWrapper
from pathlib import Path
from typing import NamedTuple

from project_file_utils import ProjectFileHeadings, read_file_to_str_list, Heading
from split_results import SplitResults, TitleDate, ProjectFileDetails

logging.basicConfig(format="%(asctime)s %(message)s")
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class FormatException(Exception):
    pass


class CommandLineArguments(NamedTuple):
    filename: str
    dry_run: bool = False
    debug: bool = False


@dataclass
class SplitState:
    week_num: str = ""
    date_str: str = ""
    project_name = ""
    project_file: TextIOWrapper = open("/dev/null")
    title: str = ""


# class TitleDate(NamedTuple):
#     title: str = ""
#     date_str: str = ""


# @dataclass
# class ProjectFileDetails:
#     name: str
#     created: bool = False
#     lines_written: dict[TitleDate, int] = field(default_factory=dict[TitleDate, int])


# @dataclass
# class SplitResults:
#     lines_processed: int = 0
#     week_num: str = ""
#     top_heading: str = ""
#     projects: dict[str, ProjectFileDetails] = field(
#         default_factory=dict[str, ProjectFileDetails]
#     )
#     days: set[str] = field(default_factory=set[str])
#
#     def __str__(self) -> str:
#         output = ""
#         output += "\n======== Split Results ========\n"
#         output += self.top_heading
#         output += "\n-------------------------------\n"
#         output += f"Processed {self.lines_processed} lines\n"
#
#         output += "Project files written to:\n"
#         for project_name, details in sorted(self.projects.items()):
#             output += f"- {project_name}\t"
#             if details.created:
#                 output += "[ CREATED ]\n"
#             else:
#                 output += "[ exists ]\n"
#         output += "-------------------------------\n"
#
#         output += "\nNotes entries written:\n"
#         for project_name, details in sorted(self.projects.items()):
#             output += f"\nProject file: {project_name}:\n"
#             for title_date, lines in details.lines_written.items():
#                 output += f'On {title_date[1]}, topic "{title_date[0]}", wrote {lines} lines\n'
#         output += "-------------------------------\n"
#
#         return output


class NoteFile:
    """
    Note file parser to parse my weekly notes and split them into separate files.

    The file is parsed to create a NoteFileStructure object which contains the structure of the file.
    """

    def __init__(self, filepath: Path):
        if not filepath.exists():
            raise FileNotFoundError(f"{filepath}")
        # TODO: add output_directory as an optional init parameter and use it instead of file_directory
        self.file_directory: Path = filepath.parent
        self.dry_run: bool = False
        self._lines: list[str] = read_file_to_str_list(filepath)

        NoteFile.validate_weekly_heading(self._lines[0])

    def split_file(self) -> SplitResults:
        """
        Split the file based on the Parsing Rules.md file

        Return the summary results in a SplitResults object
        """
        results: SplitResults = SplitResults(lines_processed=0)
        split_state: SplitState = SplitState()

        log.debug("START")

        # build the cache of project_file_headings so we can detect if the weekly file
        # has already been split
        project_file_headings: ProjectFileHeadings = ProjectFileHeadings(
            directory=self.file_directory
        )

        # loop through the lines, use 1-based line numbering to ease debugging and output
        for line_num, line in enumerate(self._lines, start=1):
            # process the first line separately as it contains the week number we need
            if line_num == 1:
                log.debug(f"line {line_num}: H1 Week heading")

                results.week_num, results.top_heading = NoteFile.process_line_1_heading(
                    line
                )
                split_state.date_str = results.week_num

            # if line is a H1 heading, then it's a new day's notes to be written
            elif line.startswith(Heading.H1):
                log.debug(f"line {line_num}: H1 heading: {line[2:]}")

                # extract the date_str from it
                split_state.date_str = NoteFile.validate_date_heading(h1_heading=line)

                # assume we're going to write a new project so
                # close the current project file (if it's open)
                split_state.project_name = ""
                split_state.project_file.close()

            # if line is a H2 heading, then it's the start of a new project note
            elif line.startswith(Heading.H2):
                log.debug(f"line {line_num}: H2 heading: {line[3:]}")

                # extract the project_name and title
                split_state.project_name, split_state.title = (
                    NoteFile.split_project_name_heading(line)
                )

                # retrieve the project details if they exist or create a new project details object
                project_details: ProjectFileDetails = results.projects.get(
                    split_state.project_name,
                    ProjectFileDetails(name=split_state.project_name),
                )

                # close the previous project file and open/create the new one for appending text
                split_state.project_file.close()

                # construct the full filepath/name for the project file
                project_filename: Path = self.file_directory / Path(
                    split_state.project_name + ".md"
                )

                # if the file already exists then just open it,
                # otherwise create it and write the project name as a H1 heading
                if (project_filename).exists():
                    if not self.dry_run:
                        split_state.project_file = open(project_filename, "a")
                    log.debug(f"File: {project_filename} EXISTS")
                    # project_details.created = False
                else:
                    if not self.dry_run:
                        split_state.project_file = open(project_filename, "a")
                    project_details.created = True
                    log.debug(f"File: {project_filename} CREATED")

                    if not self.dry_run:
                        split_state.project_file.write(
                            f"# {split_state.project_name}\n\n"
                        )

                # store the project file details in results
                results.projects[split_state.project_name] = project_details

                # use the week_num as the date if we don't have a date_str
                if split_state.date_str == "":
                    split_state.date_str = split_state.week_num

                # build the title line we want to write
                title_line: str = f"## {split_state.date_str}: {split_state.title}\n"
                log.debug(f"title_line: {title_line}")

                # check if the project file already contains the title_line and
                # skip this whole section if it does
                # FIXME: move this logic earlier when we detect we already have a project_filename existing
                if project_file_headings.contains(
                    project_filename=split_state.project_name, h2_heading=title_line
                ):
                    # set the project_name to "" so the following lines get ignored
                    log.debug(
                        f'File: {project_filename} already contains heading: "{title_line}"'
                    )
                    split_state.project_name = ""
                else:
                    # write the title line to the file
                    if not self.dry_run:
                        split_state.project_file.write(title_line)
                    project_details.lines_written[
                        TitleDate(
                            title=split_state.title, date_str=split_state.date_str
                        )
                    ] = 0

                    results.days.add(split_state.date_str)

            # if we have a project name then write the file to it
            elif split_state.project_name:
                log.debug(
                    f"line {line_num}: Appending to project: {split_state.project_name}"
                )

                if not self.dry_run:
                    split_state.project_file.write(line + "\n")

                # get the project file details, create one if it doesn't exist
                project_details = results.projects.get(
                    split_state.project_name,
                    ProjectFileDetails(name=split_state.project_name),
                )

                # get the current number of lines written to the project file for this note
                # set it to zero if we've not written to the file yet.
                lines: int = project_details.lines_written.get(
                    TitleDate(title=split_state.title, date_str=split_state.date_str), 0
                )

                # increment the number of lines written for this note
                project_details.lines_written[
                    TitleDate(title=split_state.title, date_str=split_state.date_str)
                ] = lines + 1

                # save the project details in the results
                results.projects[split_state.project_name] = project_details

            # ignore the line since we haven't handled it above
            else:
                log.debug(f"line {line_num}: IGNORED")

            results.lines_processed += 1

        split_state.project_file.close()
        log.debug("END")
        return results

    @property
    def num_lines_parsed(self) -> int:
        return len(self._lines)

    @staticmethod
    def process_line_1_heading(line: str) -> tuple[str, str]:
        return (NoteFile.validate_weekly_heading(h1_heading=line), line[2:])

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
            raise FormatException('Invalid format, expecting "## <project name>"')
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


def parse_args(argv: list[str] | None = None) -> CommandLineArguments:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Split my weekly markdown notes into separate project files"
    )
    parser.add_argument("filename", help="The file to process")
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Increase output verbosity with debug output",
    )
    parser.add_argument(
        "-s",
        "--dry-run",
        action="store_true",
        help="Simulate the split with a dry run that doesn't create or write any files",
    )
    args = parser.parse_args(argv)
    return CommandLineArguments(
        filename=args.filename, dry_run=args.dry_run, debug=args.debug
    )


def main() -> None:
    """
    This is the main entry point of the program
    """
    # Parse arguments
    args: CommandLineArguments = parse_args()

    # Create the Notefile and do the splitting
    weekly_notefile: NoteFile = NoteFile(Path(args.filename))
    if args.dry_run:
        print("** DRY RUN **")
        weekly_notefile.dry_run = args.dry_run
    results: SplitResults = weekly_notefile.split_file()
    print(results)


if __name__ == "__main__":
    main()
