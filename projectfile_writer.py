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
    h2_heading: H2Heading, date_str: str, projectfile_directory: Path
) -> ProjectFileDetails:
    project_name: str
    title: str
    project_name, title = NoteFile.split_project_name_heading(h2_heading.name)
    project_file_details: ProjectFileDetails = ProjectFileDetails(name=project_name)
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
