import shutil
from pathlib import Path
from typing import Generator

import pytest

from md_parser import NoteFile


@pytest.fixture
def temp_dir() -> Generator[Path]:
    # create the test directory
    test_dir: Path = Path("./temp_test")
    test_dir.mkdir(exist_ok=True)

    # delete all files in test directory
    file_path: Path
    for file_path in test_dir.glob("*"):
        if file_path.is_file():
            file_path.unlink()

    yield test_dir

    # delete all files in test directory
    for file_path in test_dir.glob("*"):
        if file_path.is_file():
            file_path.unlink()


@pytest.fixture
def week_1(temp_dir: Path) -> Generator[NoteFile]:
    # specify the file and the directory to work in
    src_md_filepath: Path = Path("tests/Test Week 1.md")

    # copy the weekly file to test directory
    md_filepath: Path = temp_dir / src_md_filepath.name
    shutil.copy(src_md_filepath, md_filepath)

    # load the file
    note_file: NoteFile = NoteFile(md_filepath)

    yield note_file


@pytest.fixture
def week_2(temp_dir: Path) -> Generator[NoteFile]:
    # specify the file and the directory to work in
    src_md_filepath: Path = Path("tests/Test Week 2.md")

    # copy the weekly file to test directory
    md_filepath: Path = temp_dir / src_md_filepath.name
    shutil.copy(src_md_filepath, md_filepath)

    # load the file
    note_file: NoteFile = NoteFile(md_filepath)

    yield note_file
