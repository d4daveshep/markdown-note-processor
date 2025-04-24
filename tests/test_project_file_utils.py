from pathlib import Path
from project_file_utils import read_file_to_str_list


def test_read_file_to_str_list():
    project_file_path: Path = Path("./tests/week_2_files/Project 1.md")
    assert project_file_path.exists()

    lines: list[str] = read_file_to_str_list(file=project_file_path)
    assert len(lines) == 33


def test_project_file_contains_h2_heading():
    assert False, "implement me"
