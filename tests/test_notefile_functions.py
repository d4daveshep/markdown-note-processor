import pytest

from md_parser import FormatException, NoteFile, SplitResults


def test_load_notefile(week_1: NoteFile):
    assert week_1.num_lines_parsed == 54


def test_split_file(week_1: NoteFile):
    results: SplitResults = week_1.split_file()
    assert results.lines_procesed == 54


@pytest.mark.parametrize(
    "heading, expected_project_name, expected_title",
    [
        ("# Project Name - This note title", "Project Name", "This note title"),
        (
            "# Project Name - This note title - with a hyphen",
            "Project Name",
            "This note title - with a hyphen",
        ),
        ("# Project Name Only", "Project Name Only", ""),
    ],
)
def test_split_project_name_heading(
    heading: str, expected_project_name: str, expected_title: str
):
    project_name, title = NoteFile.split_project_name_heading(heading)
    assert project_name == expected_project_name
    assert title == expected_title


@pytest.mark.parametrize(
    "heading",
    [
        ("#"),
        ("# "),
        ("# -"),
    ],
)
def test_split_invalid_project_name_heading(heading: str):
    with pytest.raises(FormatException):
        project_name, title = NoteFile.split_project_name_heading(heading)


def test_validate_weekly_heading():
    valid_h1: list[str] = [
        "# W01 2023: This is a valid string",
        "# W52 2024: Another valid string",
    ]
    for heading in valid_h1:
        assert NoteFile.validate_weekly_heading(heading)

    invalid_h1: list[str] = [
        "# W00 2023: Invalid - week number out of range",
        "# W53 2023: Invalid - week number out of range",
        "# W12 23: Invalid - year isn't 4 digits",
        " # W12 2023: Invalid - doesn't start at beginning of string",
        "# w12 2023: Invalid - 'W' must be uppercase",
    ]
    for heading in invalid_h1:
        with pytest.raises(FormatException):
            NoteFile.validate_weekly_heading(heading)
