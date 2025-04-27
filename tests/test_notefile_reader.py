from notefile_reader import load_weekly_note_file, WeeklyNotes, H1Heading, H2Heading
from pathlib import Path


def test_notefile_reader():
    week_1_file: Path = Path("tests/week_1_files/Test Week 1.md")
    weekly_notes: WeeklyNotes = load_weekly_note_file(file=week_1_file)
    assert len(weekly_notes.h1_headings) == 5
    assert weekly_notes.h1_headings[0].name == "# Week 01 2025: 1 Jan - 7 Jan"
    assert weekly_notes.h1_headings[2].name == "# Thu 02 Jan 2025"


def test_h1_heading():
    h1: H1Heading = H1Heading("test line")
    assert h1.name == "test line"
    assert h1.lines == []
    assert h1.h2_headings == []


def test_h2_heading():
    h2: H2Heading = H2Heading("test h2 heading")
    assert h2.name == "test h2 heading"
    assert h2.lines == []
