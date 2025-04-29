from pathlib import Path
from project_file_utils import (
    read_file_to_str_list,
    get_h2_headings,
    ProjectFileHeadings,
)


def test_read_file_to_str_list(project_file_1: Path):
    lines: list[str] = read_file_to_str_list(filepath=project_file_1)
    assert len(lines) == 33


def test_project_file_h2_headings(project_file_1: Path):
    """
    Test we can get the set of h2 headings in a project file
    """
    h2_headings: set[str] = get_h2_headings(project_file_1)
    assert len(h2_headings) == 5

    h2_heading: str = "## Mon 08 Jan 2025: Second week on this project"
    assert h2_heading in h2_headings


def test_project_files_h2_headings_class():
    project_file_directory: Path = Path("tests/week_2_files/")
    project_file_headings: ProjectFileHeadings = ProjectFileHeadings(
        project_file_directory
    )

    assert len(project_file_headings._cache) == 7
    assert "Project 3" in project_file_headings._cache
    assert len(project_file_headings._cache["Project 3"]) == 3

    assert project_file_headings.contains(
        project_filename="Project 1",
        h2_heading="## Mon 08 Jan 2025: Second week on this project",
    )

    assert not project_file_headings.contains(
        project_filename="Non-existent file", h2_heading=""
    )

    assert not project_file_headings.contains(
        project_filename="Project 1",
        h2_heading="## No such heading",
    )


def test_project_file_headings_class_is_a_singleton():
    project_file_directory: Path = Path("tests/week_2_files/")
    instance_1: ProjectFileHeadings = ProjectFileHeadings(project_file_directory)
    instance_2: ProjectFileHeadings = ProjectFileHeadings(project_file_directory)
    assert instance_1 is instance_2
