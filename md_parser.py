from enum import StrEnum
from pathlib import Path


class Heading(StrEnum):
    H1 = "# "
    H2 = "## "


class MDParser:
    def __init__(self, filepath: Path):
        if not filepath.exists():
            raise FileNotFoundError(f"{filepath}")
        with open(filepath, "r") as file:
            data: str = file.read()
            self._lines: list[str] = data.split("\n")

    def heading_line_numbers(self, heading: Heading) -> list[int]:
        line_nums: list[int] = []
        for line_num, line in enumerate(self._lines):
            if line.startswith(heading):
                line_nums.append(line_num)
        return line_nums

    @property
    def num_lines_parsed(self) -> int:
        return len(self._lines)
