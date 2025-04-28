from projectfile_writer import write_project_files
from split_results import SplitResults
from tests.conftest import temp_dir
from weekly_notes import WeeklyNotes


def test_write_project_files(week_1_notes: WeeklyNotes):
    results: SplitResults = write_project_files(week_1_notes)
    assert results.lines_processed == week_1_notes.total_lines


def test_write_project_file(week_1_notes: WeeklyNotes):
    h1_heading = week_1_notes.h1_headings[2]
    h2_heading = h1_heading.h2_headings[2]

    projectfile_details: ProjectFileDetails = write_projectfile(
        h2_heading, temp_dir, projectfile_headings
    )
