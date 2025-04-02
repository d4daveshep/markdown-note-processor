from pathlib import Path

import pytest

from md_parser import Heading, MDParser


@pytest.fixture
def week_1() -> MDParser:
    md_filepath: Path = Path("tests/Test Week 1.md")
    md_parser: MDParser = MDParser(md_filepath)
    return md_parser


def test_load_file() -> None:
    md_filepath: Path = Path("tests/Test Week 1.md")
    assert md_filepath.exists()
    md_parser: MDParser = MDParser(md_filepath)
    assert md_parser
    assert md_parser.num_lines_parsed == 54


def test_load_nonexistent_file() -> None:
    with pytest.raises(FileNotFoundError) as err:
        _: MDParser = MDParser(Path("no such file.txt"))
    assert "no such file" in str(err.value)


def test_find_heading_line_numbers() -> None:
    md_filepath: Path = Path("tests/Test Week 1.md")
    md_parser: MDParser = MDParser(md_filepath)

    h1_lines: list[int] = md_parser.heading_line_numbers(Heading.H1)
    assert len(h1_lines) == 5
    assert h1_lines == [0, 6, 16, 40, 44]

    h2_lines: list[int] = md_parser.heading_line_numbers(Heading.H2)
    assert len(h2_lines) == 8


# def test_heading_structure(week_1: MDParser) -> None:
# assert week_1.h1[0].


def file_weekly_notes(md_filepath: Path) -> None:
    pass
    # parse the file into MDParser
    # check h1[0] is a valid weekly date range format (W12 23 Mar - 31 Mar 2025)
    # process any h2s within h1[0]

    # for each h1
    # check if it's a day (ddd dd mmm yyyy)
    # store as h1.date
    # for each h2 within the h1
    # get the project/name up to the hyphen (h2.project_name)
    # get the note title beyone the hyphen (h2.title)
    # it's OK if h2.title == ""
    # find/create the project/name file
    # if creating, then start with h2.project_name as h1
    # append the h1.date - h2.title (as h2)
    # append all the lines up to the next h1
    # close the file
