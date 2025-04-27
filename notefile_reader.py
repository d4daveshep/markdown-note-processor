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
    in_h1: bool = False
    in_h2: bool = False

    lines: list[str] = read_file_to_str_list(file)
    for line in lines:
        if line.startswith(Heading.H1):
            in_h1 = True
            h1_heading: H1Heading = H1Heading(line)
            weekly_notes.h1_headings.append(h1_heading)
        if line.startswith(Heading.H2):
            in_h2 = True
            h2_heading: H2Heading = H2Heading(line)
            h1_heading.h2_headings.append(h2_heading)

    return weekly_notes
