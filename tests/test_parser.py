from pathlib import Path

import pytest

from md_parser import Heading, NoteFile


def test_load_file() -> None:
    md_filepath: Path = Path("tests/Test Week 1.md")
    assert md_filepath.exists()
    md_parser: NoteFile = NoteFile(md_filepath)
    assert md_parser
    assert md_parser.num_lines_parsed == 54


def test_load_nonexistent_file() -> None:
    with pytest.raises(FileNotFoundError) as err:
        _: NoteFile = NoteFile(Path("no such file.txt"))
    assert "no such file" in str(err.value)


def test_get_heading_line_numbers(week_1: NoteFile) -> None:
    h1_lines: list[int] = week_1.heading_line_numbers(Heading.H1)
    assert len(h1_lines) == 5
    assert h1_lines == [0, 6, 16, 40, 44]

    h2_lines: list[int] = week_1.heading_line_numbers(Heading.H2)
    assert len(h2_lines) == 8


# def test_analyse_structure(week_1: NoteFile) -> None:
#     file_structure: NoteFileStructure = week_1.analyse_structure()
#     assert file_structure.line_count == 54
#     assert len(file_structure.h1_headings) == 5
#     assert False, "write some more tests"


def test_h2_lines_in_h1(week_1: NoteFile) -> None:
    assert week_1.h2_lines_in_h1(h1_index=0) == [(2, 5)]
    assert week_1.h2_lines_in_h1(h1_index=1) == [8, 12]
    assert week_1.h2_lines_in_h1(h1_index=2) == [18, 22, 36]
    assert week_1.h2_lines_in_h1(h1_index=3) == []
    assert week_1.h2_lines_in_h1(h1_index=4) == [46, 56]


def file_weekly_notes(md_filepath: Path) -> None:
    pass
    # parse the file into NoteFile
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
