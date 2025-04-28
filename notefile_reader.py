import logging
from dataclasses import dataclass, field
from pathlib import Path

from project_file_utils import Heading, read_file_to_str_list

logging.basicConfig(format="%(asctime)s %(message)s")
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


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
        self.total_lines: int = 0

    def count_lines_saved(self) -> int:
        count: int = 0
        # count += len(self.h1_headings)
        # count += sum(len(h1.lines) for h1 in self.h1_headings)
        for h1 in self.h1_headings:
            count += 1
            count += len(h1.lines)
            for h2 in h1.h2_headings:
                count += 1
                count += len(h2.lines)
        return count


def load_weekly_note_file(file: Path) -> WeeklyNotes:
    weekly_notes: WeeklyNotes = WeeklyNotes()
    in_h1: bool = False
    in_h2: bool = False

    lines: list[str] = read_file_to_str_list(file)
    weekly_notes.total_lines = len(lines)

    for line_num, line in enumerate(lines):
        log.debug(f"line {line_num}: {line}")
        if line.startswith(Heading.H1):
            in_h1 = True
            in_h2 = False
            h1_heading: H1Heading = H1Heading(line)
            weekly_notes.h1_headings.append(h1_heading)
            log.debug("H1 heading added")
        elif line.startswith(Heading.H2):
            in_h2 = True
            h2_heading: H2Heading = H2Heading(line)
            if in_h1:
                h1_heading.h2_headings.append(h2_heading)
                log.debug("H2 heading added")
        else:
            # not a H1 or H2 heading, so save it in teh corect place
            if in_h2:
                h2_heading.lines.append(line)
                log.debug("line added to H2")
            elif in_h1:
                h1_heading.lines.append(line)
                log.debug("line added to H1")
            else:
                log.debug("line IGNORED")
                pass

    return weekly_notes
