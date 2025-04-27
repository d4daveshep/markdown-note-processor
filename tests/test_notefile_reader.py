from pathlib import Path
from dataclasses import dataclass, field

from project_file_utils import read_file_to_str_list, Heading


@dataclass
class H2Heading:
    name: str
    lines: list[str] = field(default_factory=list[str])


@dataclass
class H1Heading:
    name: str
    h2_headings: list[H2Heading] = field(default_factory=list[H2Heading])
    lines: list[str] = field(default_factory=list[str])


class WeeklyNotes:
    def __init__(self) -> None:
        self.h1_headings: list[H1Heading] = []


def load_weekly_note_file(file: Path) -> WeeklyNotes:
    weekly_notes: WeeklyNotes = WeeklyNotes()
    lines: list[str] = read_file_to_str_list(file)
    for line in lines:
        if line.startswith(Heading.H1):
            h1_heading: H1Heading = H1Heading(line)
            weekly_notes.h1_headings.append(h1_heading)
    return weekly_notes


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
