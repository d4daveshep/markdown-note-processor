from enum import StrEnum
from pathlib import Path


class Heading(StrEnum):
    H1 = "H1"
    H2 = "H2"


class MDParser:
    def __init__(self, filepath: Path):
        pass

    def find_next(self, heading: Heading) -> str:
        return ""
