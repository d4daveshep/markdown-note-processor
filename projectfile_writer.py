from io import TextIOWrapper
import logging
from md_parser import NoteFile, ProjectFileDetails
from pathlib import Path

from project_file_utils import ProjectFileHeadings
from split_results import SplitResults
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
    file_created: bool = False

    # extract the project name and title
    project_name, title = NoteFile.split_project_name_heading(h2_heading.name)
    log.debug(f"project name = {project_name}, title = {title}")

    # construct the full file path and name of the project file we'll write to
    project_filepath: Path = project_directory / Path(project_name + ".md")

    # build the title line we want to write
    title_line: str = f"## {date_str}: {title}\n"
    log.debug(f"title_line = {title_line}")

    # if the file exists and doesn't contain the title line already, then open it
    if project_filepath.exists():
        log.debug(f"{project_filepath} already EXISTS")
        if not existing_project_file_headings.contains(project_name, title_line):
            project_file = open(project_filepath, "a")

        else:
            log.debug(
                f"... and already contains {title_line} so SKIPPING this whole heading"
            )
            return

    # but if the file doesn't exist open it (which creates it)
    else:
        log.debug(f"{project_filepath} CREATED")
        project_file = open(project_filepath, "a")
        file_created = True

    # create the project file details and enter the info so far
    project_file_details: ProjectFileDetails = ProjectFileDetails(name=project_name)
    project_file_details.created = file_created

    # write the heading line to the file
    project_file.write(f"# {project_name}\n\n")

    # TODO: write the lines here

    return project_file_details


def write_project_files(
    weekly_notes: WeeklyNotes, projectfile_directory: Path
) -> SplitResults:
    results: SplitResults = SplitResults(lines_processed=0)

    log.debug("START")

    # build the cache of project_file_headings so we can detect if the weekly file
    # has already been split
    projectfile_headings: ProjectFileHeadings = ProjectFileHeadings(
        directory=projectfile_directory
    )

    # loop throuugh the H1 headings...
    for h1_heading_num, h1_heading in enumerate(weekly_notes.h1_headings):
        # get the weekly date range from the first H1 heading
        if h1_heading_num == 0:
            NoteFile.validate_weekly_heading(h1_heading.name)
            weekly_date_str: str = h1_heading.name[2:]

            for h2_heading in h1_heading.h2_headings:
                write_project_file(h2_heading, weekly_date_str, projectfile_directory)

        else:
            date_str: str = NoteFile.validate_date_heading(h1_heading.name)

    return results
