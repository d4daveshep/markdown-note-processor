from pathlib import Path

import pytest

from md_parser import NoteFile


@pytest.fixture
def week_1() -> NoteFile:
    md_filepath: Path = Path("tests/Test Week 1.md")
    md_parser: NoteFile = NoteFile(md_filepath)
    return md_parser
