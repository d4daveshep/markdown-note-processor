import filecmp
from pathlib import Path

from md_parser import ProjectFileDetails
from projectfile_writer import write_project_file, write_project_files
from split_results import SplitResults, TitleDate
from weekly_notes import H2Heading, WeeklyNotes, H1Heading


def test_write_project_files(week_1_notes: WeeklyNotes, temp_dir: Path):
    results: SplitResults = write_project_files(week_1_notes, temp_dir)
    assert results.lines_processed == week_1_notes.total_lines


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
    assert filecmp.cmp(Path("./tests/week_1_files/Project 2.md"), project_filepath), (
        f"{project_filepath.name} differs"
    )
