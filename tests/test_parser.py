from pathlib import Path

import pytest

from md_parser import NoteFile


def test_load_file() -> None:
    md_filepath: Path = Path("tests/week_1_files/Test Week 1.md")
    assert md_filepath.exists()
    md_parser: NoteFile = NoteFile(md_filepath)
    assert md_parser
    assert md_parser.num_lines_parsed == 54


def test_load_nonexistent_file() -> None:
    with pytest.raises(FileNotFoundError) as err:
        _: NoteFile = NoteFile(Path("no such file.txt"))
    assert "no such file" in str(err.value)
