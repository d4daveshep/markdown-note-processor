from pathlib import Path
from project_file_utils import read_file_to_str_list, get_h2_headings


def test_read_file_to_str_list(project_file_1: Path):
    lines: list[str] = read_file_to_str_list(file=project_file_1)
    assert len(lines) == 33


def test_project_file_h2_headings(project_file_1: Path):
    """
    Test we can get the set of h2 headings in a project file
    """
    h2_headings: list[str] = get_h2_headings(project_file_1)
    assert len(h2_headings) == 5

    h2_heading: str = "## Mon 08 Jan 2025: Second week on this project"
    assert h2_heading in h2_headings
