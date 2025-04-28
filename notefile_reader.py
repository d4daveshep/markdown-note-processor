import logging
from pathlib import Path

from project_file_utils import Heading, read_file_to_str_list
from weekly_notes import H1Heading, H2Heading, WeeklyNotes

logging.basicConfig(format="%(asctime)s %(message)s")
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


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
