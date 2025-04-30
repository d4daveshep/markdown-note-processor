import logging
import argparse
from typing import NamedTuple
import re
from datetime import datetime
from io import TextIOWrapper
from pathlib import Path

from notefile_reader import load_weekly_note_file
from project_file_utils import ProjectFileHeadings
from split_results import SplitResults, TitleDate, ProjectFileDetails
from weekly_notes import H2Heading, WeeklyNotes

logging.basicConfig(format="%(asctime)s %(message)s")
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class FormatException(Exception):
    pass


class CommandLineArguments(NamedTuple):
    filename: str
    output_dir: str = ""
    dry_run: bool = False
    debug: bool = False


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


def write_project_file(
    h2_heading: H2Heading, date_str: str, project_directory: Path, dry_run: bool = False
) -> ProjectFileDetails:
    """
    Write a project file entry from the weekly note H2 heading.

    Return a ProjectFileDetails object
    """

    # define some variables we'll need
    project_name: str
    title: str
    project_file: TextIOWrapper
    existing_project_file_headings: ProjectFileHeadings = ProjectFileHeadings(
        directory=project_directory
    )

    # extract the project name and title
    project_name, title = split_project_name_heading(h2_heading.name)
    log.debug(f"project name = {project_name}, title = {title}")

    # create the project file details
    project_file_details: ProjectFileDetails = ProjectFileDetails(name=project_name)

    # construct the full file path and name of the project file we'll write to
    project_filepath: Path = project_directory / Path(project_name + ".md")

    # build the title line we want to write
    title_line: str = f"## {date_str}: {title}"
    log.debug(f"title_line = {title_line}")

    # if the file exists and doesn't contain the title line already, then open it
    if project_filepath.exists():
        log.debug(f"{project_filepath} already EXISTS")
        project_file_details.created = False

        if existing_project_file_headings.contains(project_name, title_line):
            log.debug(
                f"... and already contains {title_line} so SKIPPING this whole heading"
            )
            return project_file_details

        elif not dry_run:
            project_file = open(project_filepath, "a")

    # but if the file doesn't exist open it (which creates it)
    else:
        log.debug(f"{project_filepath} CREATED")
        if not dry_run:
            project_file = open(project_filepath, "a")
        project_file_details.created = True

        # write the heading line to the file
        if not dry_run:
            project_file.write(f"# {project_name}\n\n")

    # write the title line
    if not dry_run:
        project_file.write(title_line + "\n")

    # write the lines to the file
    if not dry_run:
        for line in h2_heading.lines:
            project_file.write(line + "\n")

    project_file_details.lines_written[TitleDate(title, date_str)] = len(
        h2_heading.lines
    )

    if not dry_run:
        project_file.close()

    return project_file_details


def write_project_files(
    weekly_notes: WeeklyNotes, project_directory: Path, dry_run: bool = False
) -> SplitResults:
    results: SplitResults = SplitResults()

    log.debug("START")

    # loop throuugh the H1 headings...
    for h1_heading_num, h1_heading in enumerate(weekly_notes.h1_headings):
        # write the "week-long" project notes
        if h1_heading_num == 0:
            validate_weekly_heading(h1_heading.name)
            weekly_date_str: str = h1_heading.name[2:]
            results.week_num = weekly_date_str

            # write to the project files for "week-long" projects
            for h2_heading in h1_heading.h2_headings:
                project_file_details: ProjectFileDetails = write_project_file(
                    h2_heading, weekly_date_str, project_directory, dry_run
                )

                # merge the results
                results.merge_project_file_details(project_file_details)

        # write the project files for all daily notes
        else:
            date_str: str = validate_date_heading(h1_heading.name)

            # write to the project files for "week-long" projects
            for h2_heading in h1_heading.h2_headings:
                project_file_details: ProjectFileDetails = write_project_file(
                    h2_heading, date_str, project_directory, dry_run
                )

                # merge the results
                results.merge_project_file_details(project_file_details)

    return results


def parse_args(argv: list[str] | None = None) -> CommandLineArguments:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Split my weekly markdown notes into separate project files"
    )
    parser.add_argument("filename", help="The weekly notes file to process")
    parser.add_argument(
        "-o",
        "--output_dir",
        help="The directory to write the project files in (default=same diretory as note file)",
    )
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
        filename=args.filename,
        output_dir=args.output_dir,
        dry_run=args.dry_run,
        debug=args.debug,
    )


def main() -> None:
    """
    This is the main entry point of the program
    """
    # Parse arguments
    args: CommandLineArguments = parse_args()

    note_file: Path = Path(args.filename)
    output_dir: Path = note_file.parent

    # read the note file
    weekly_notes: WeeklyNotes = load_weekly_note_file(file=note_file)

    # get the output_dir
    if args.output_dir:
        output_dir = Path(args.output_dir)

    if args.dry_run:
        print("** DRY RUN **")

    results: SplitResults = write_project_files(
        weekly_notes=weekly_notes, project_directory=output_dir, dry_run=args.dry_run
    )
    print(results)


if __name__ == "__main__":
    main()
