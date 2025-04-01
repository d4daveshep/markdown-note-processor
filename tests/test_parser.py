from pathlib import Path

from md_parser import Heading, MDParser


def test_load_file() -> None:
    md_filepath: Path = Path("tests/Test Week 1.md")
    assert md_filepath.exists()


def test_find_h1_text() -> None:
    md_filepath: Path = Path("tests/Test Week 1.md")
    md_parser: MDParser = MDParser(md_filepath)

    h1: str = md_parser.find_next(heading=Heading.H1)
    assert h1
