from pathlib import Path

from md_parser import ProjectFileDetails
from projectfile_writer import write_project_file, write_project_files
from split_results import SplitResults, TitleDate
from weekly_notes import H2Heading, WeeklyNotes


def test_write_project_files(week_1_notes: WeeklyNotes, temp_dir: Path):
    results: SplitResults = write_project_files(week_1_notes, temp_dir)
    assert results.lines_processed == week_1_notes.total_lines


def test_write_project_file(week_1_notes: WeeklyNotes, temp_dir: Path):
    date_str: str = "Thu 02 Jan 2025"
    h2_heading: H2Heading = H2Heading(name="## Project 3 - Starting on day 2")

    h2_heading.lines.append("")
    h2_heading.lines.append("Some notes from project 3 on day 2")
    h2_heading.lines.append("")

    project_file_details: ProjectFileDetails = write_project_file(
        h2_heading=h2_heading,
        date_str=date_str,
        projectfile_directory=temp_dir,
    )
    assert project_file_details.name == "Project 3"
    assert project_file_details.created
    assert (
        TitleDate(title="Starting on day 2", date_str=date_str)
        in project_file_details.lines_written
    )
