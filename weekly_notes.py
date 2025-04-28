from dataclasses import dataclass, field


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
        for h1 in self.h1_headings:
            count += 1
            count += len(h1.lines)
            for h2 in h1.h2_headings:
                count += 1
                count += len(h2.lines)
        return count
