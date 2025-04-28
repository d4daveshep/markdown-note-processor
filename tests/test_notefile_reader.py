import logging
import pytest
from pathlib import Path
from weekly_notes import WeeklyNotes, H1Heading, H2Heading
from notefile_reader import load_weekly_note_file

logging.basicConfig(format="%(asctime)s %(message)s")
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


@pytest.fixture
def week_1_notes() -> WeeklyNotes:
    week_1_file: Path = Path("tests/week_1_files/Test Week 1.md")
    week_1_notes: WeeklyNotes = load_weekly_note_file(file=week_1_file)
    return week_1_notes


def test_notefile_reader(week_1_notes: WeeklyNotes):
    assert len(week_1_notes.h1_headings) == 5
    assert week_1_notes.total_lines == 54

    h1_heading_0: H1Heading = week_1_notes.h1_headings[0]
    assert h1_heading_0.name == "# Week 01 2025: 1 Jan - 7 Jan"
    assert len(h1_heading_0.lines) == 1
    assert len(h1_heading_0.h2_headings) == 1

    h2_heading: H2Heading = h1_heading_0.h2_headings[0]
    assert h2_heading.name == "## Project 0 - All week long"
    assert len(h2_heading.lines) == 3
    assert h2_heading.lines[1] == "This is an item prior to day 1."

    h1_heading_2: H1Heading = week_1_notes.h1_headings[2]
    assert h1_heading_2.name == "# Thu 02 Jan 2025"
    assert len(h1_heading_2.lines) == 1
    assert len(h1_heading_2.h2_headings) == 3


def test_h1_heading():
    h1: H1Heading = H1Heading("test line")
    assert h1.name == "test line"
    assert h1.lines == []
    assert h1.h2_headings == []

    h1.h2_headings.append(H2Heading("h2 heading"))
    h1.lines.append("a new line")
    assert len(h1.h2_headings) == 1
    assert len(h1.lines) == 1


def test_h2_heading():
    h2: H2Heading = H2Heading("test h2 heading")
    assert h2.name == "test h2 heading"
    assert h2.lines == []


def test_notefile_reader_count_lines_saved(week_1_notes: WeeklyNotes):
    assert week_1_notes.count_lines_saved() == week_1_notes.total_lines
