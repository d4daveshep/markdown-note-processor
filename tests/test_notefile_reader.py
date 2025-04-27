from pathlib import Path
from dataclasses import dataclass

from project_file_utils import read_file_to_str_list, Heading


@dataclass
class H1Heading:
    pass


class WeeklyNotes:
    def __init__(self) -> None:
        self.h1_headings: list[H1Heading] = []


def load_weekly_note_file(file: Path) -> WeeklyNotes:
    weekly_notes: WeeklyNotes = WeeklyNotes()
    lines: list[str] = read_file_to_str_list(file)
    for line in lines:
        if line.startswith(Heading.H1):
            h1_heading: H1Heading = H1Heading()
            weekly_notes.h1_headings.append(h1_heading)
    return weekly_notes


def test_notefile_reader():
    week_1_file: Path = Path("tests/week_1_files/Test Week 1.md")
    weekly_notes: WeeklyNotes = load_weekly_note_file(file=week_1_file)
    assert len(weekly_notes.h1_headings) == 5


def test_h1_heading():
    h1: H1Heading = H1Heading()
    assert h1
