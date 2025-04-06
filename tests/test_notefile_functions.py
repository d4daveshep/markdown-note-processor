from pathlib import Path

import pytest

from md_parser import FormatException, NoteFile, SplitResults


def test_load_notefile(week_1: NoteFile) -> None:
    assert week_1.file_directory == Path("./temp_test")
    assert week_1.num_lines_parsed == 54


def test_split_file(week_1: NoteFile) -> None:
    results: SplitResults = week_1.split_file()
    assert results.lines_procesed == 54


@pytest.mark.parametrize(
    "h2_heading, expected_project_name, expected_title",
    [
        ("## Project Name - This note title", "Project Name", "This note title"),
        (
            "## Project Name - This note title - with a hyphen",
            "Project Name",
            "This note title - with a hyphen",
        ),
        ("## Project Name Only", "Project Name Only", ""),
    ],
)
def test_split_project_name_heading(
    h2_heading: str, expected_project_name: str, expected_title: str
) -> None:
    project_name, title = NoteFile.split_project_name_heading(h2_heading)
    assert project_name == expected_project_name
    assert title == expected_title


@pytest.mark.parametrize(
    "h2_heading",
    [
        ("##"),
        ("## "),
        ("## -"),
    ],
)
def test_split_invalid_project_name_heading(h2_heading: str) -> None:
    with pytest.raises(FormatException):
        project_name, title = NoteFile.split_project_name_heading(h2_heading)


@pytest.mark.parametrize(
    "h1_heading, week_num",
    [
        ("# W01 2023: This is a valid string", "W01 2023"),
        ("# W01 2023: This is a valid string", "W01 2023"),
    ],
)
def test_validate_weekly_heading(h1_heading: str, week_num: str) -> None:
    assert NoteFile.validate_weekly_heading(h1_heading) == week_num

    invalid_h2: list[str] = [
        "# W00 2023: Invalid - week number out of range",
        "# W53 2023: Invalid - week number out of range",
        "# W12 23: Invalid - year isn't 4 digits",
        " # W12 2023: Invalid - doesn't start at beginning of string",
        "# w12 2023: Invalid - 'W' must be uppercase",
    ]
    for heading in invalid_h2:
        with pytest.raises(FormatException):
            NoteFile.validate_weekly_heading(heading)


@pytest.mark.parametrize("heading", [("# Mon 6 Jan 2025"), ("# Fri 28 Mar 2025")])
def test_validate_date_heading(heading: str) -> None:
    date_str: str = NoteFile.validate_date_heading(heading)
    assert date_str == heading[2:]


@pytest.mark.parametrize(
    "heading",
    [
        ("# "),
    ],
)
def test_invalid_date_heading(heading: str) -> None:
    with pytest.raises(FormatException):
        NoteFile.validate_date_heading(heading)


def test_ignore_non_date_heading() -> None:
    assert NoteFile.validate_date_heading("# Not a date") == ""


def test_notefile_directory_property(week_1: NoteFile) -> None:
    assert week_1.file_directory == Path("temp_test/")
