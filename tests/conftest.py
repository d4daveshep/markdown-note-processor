import shutil
from pathlib import Path

import pytest

from md_parser import NoteFile


@pytest.fixture
def temp_dir() -> Path:
    # create the test directory
    test_dir: Path = Path("./temp_test")
    test_dir.mkdir(exist_ok=True)

    # delete all files in test directory
    file_path: Path
    for file_path in test_dir.glob("*"):
        if file_path.is_file():
            file_path.unlink()

    return test_dir


@pytest.fixture
def week_1(temp_dir: Path) -> NoteFile:
    # specify the file and the directory to work in
    src_md_filepath: Path = Path("tests/Test Week 1.md")

    # copy the weekly file to test directory
    md_filepath: Path = temp_dir / src_md_filepath.name
    shutil.copy(src_md_filepath, md_filepath)

    # load the file
    note_file: NoteFile = NoteFile(md_filepath)

    return note_file
