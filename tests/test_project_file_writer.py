import filecmp
from pathlib import Path

from weekly_note_processor.project_file_utils import ProjectFileHeadings
from weekly_note_processor.project_file_writer import write_project_file, write_project_files
from weekly_note_processor.split_results import ProjectFileDetails, SplitResults, TitleDate
from weekly_note_processor.weekly_notes import H1Heading, H2Heading, WeeklyNotes


def test_write_project_files(week_1_notes: WeeklyNotes, temp_dir: Path):
    existing_project_file_headings: ProjectFileHeadings = ProjectFileHeadings(
        directory=temp_dir
    )
    existing_project_file_headings.reload(temp_dir)

    results: SplitResults = write_project_files(week_1_notes, temp_dir)
    assert results.total_lines_written == 34


def test_write_project_file(week_1_notes: WeeklyNotes, temp_dir: Path):
    """
    # Wed 01 Jan 2025

    ## Project 1 - First project day

    This is an item from day 1 of project 1.

    """

    h1_heading: H1Heading = week_1_notes.h1_headings[1]
    date_str: str = h1_heading.name[2:]
    assert date_str == "Wed 01 Jan 2025"

    h2_heading: H2Heading = h1_heading.h2_headings[1]
    print(h2_heading)

    project_file_details: ProjectFileDetails = write_project_file(
        h2_heading=h2_heading,
        date_str=date_str,
        project_directory=temp_dir,
    )
    assert project_file_details.name == "Project 2"
    assert project_file_details.created
    assert (
        TitleDate(title="Another first entry", date_str=date_str)
        in project_file_details.lines_written
    )

    # check file is as expected
    project_filepath: Path = Path(temp_dir) / Path(project_file_details.name + ".md")
    assert project_filepath.exists()
    assert filecmp.cmp(Path("./test_data/week_1_files/Project 2.md"), project_filepath), (
        f"{project_filepath.name} differs"
    )
