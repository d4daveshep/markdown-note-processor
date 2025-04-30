from io import TextIOWrapper
import logging
from md_parser import NoteFile, ProjectFileDetails
from pathlib import Path

from project_file_utils import ProjectFileHeadings
from split_results import SplitResults, TitleDate
from weekly_notes import H2Heading, WeeklyNotes

logging.basicConfig(format="%(asctime)s %(message)s")
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def write_project_file(
    h2_heading: H2Heading, date_str: str, project_directory: Path
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
    project_name, title = NoteFile.split_project_name_heading(h2_heading.name)
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
        if not existing_project_file_headings.contains(project_name, title_line):
            project_file = open(project_filepath, "a")

        else:
            log.debug(
                f"... and already contains {title_line} so SKIPPING this whole heading"
            )
            return project_file_details

    # but if the file doesn't exist open it (which creates it)
    else:
        log.debug(f"{project_filepath} CREATED")
        project_file = open(project_filepath, "a")
        project_file_details.created = True

        # write the heading line to the file
        project_file.write(f"# {project_name}\n\n")

    # write the title line
    project_file.write(title_line + "\n")

    # write the lines to the file
    for line in h2_heading.lines:
        project_file.write(line + "\n")

    project_file_details.lines_written[TitleDate(title, date_str)] = len(
        h2_heading.lines
    )

    project_file.close()

    return project_file_details


def write_project_files(
    weekly_notes: WeeklyNotes, project_directory: Path
) -> SplitResults:
    results: SplitResults = SplitResults()

    log.debug("START")

    # loop throuugh the H1 headings...
    for h1_heading_num, h1_heading in enumerate(weekly_notes.h1_headings):
        # write the "week-long" project notes
        if h1_heading_num == 0:
            NoteFile.validate_weekly_heading(h1_heading.name)
            weekly_date_str: str = h1_heading.name[2:]
            results.week_num = weekly_date_str

            # write to the project files for "week-long" projects
            for h2_heading in h1_heading.h2_headings:
                project_file_details: ProjectFileDetails = write_project_file(
                    h2_heading, weekly_date_str, project_directory
                )

                # merge the results
                results.merge_project_file_details(project_file_details)

        # write the project files for all daily notes
        else:
            date_str: str = NoteFile.validate_date_heading(h1_heading.name)

            # write to the project files for "week-long" projects
            for h2_heading in h1_heading.h2_headings:
                project_file_details: ProjectFileDetails = write_project_file(
                    h2_heading, date_str, project_directory
                )

                # merge the results
                results.merge_project_file_details(project_file_details)

    return results
