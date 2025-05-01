import shutil
from pathlib import Path
from typing import Generator

import pytest

from weekly_note_file_reader import load_weekly_note_file
from weekly_notes import WeeklyNotes


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
    # for file_path in test_dir.glob("*"):
    #     if file_path.is_file():
    #         file_path.unlink()


@pytest.fixture
def project_file_1() -> Path:
    project_file: Path = Path("tests/week_2_files/Project 1.md")
    assert project_file.exists()
    return project_file


@pytest.fixture
def week_1_notes(temp_dir: Path) -> Generator[WeeklyNotes]:
    # specify the file and the directory to work in
    src_filepath: Path = Path("tests/week_1_files/Test Week 1.md")

    # copy the weekly file to test directory
    dst_filepath: Path = temp_dir / src_filepath.name
    shutil.copy(src_filepath, dst_filepath)

    week_1_notes: WeeklyNotes = load_weekly_note_file(file=dst_filepath)
    yield week_1_notes


@pytest.fixture
def week_2_notes(temp_dir: Path) -> Generator[WeeklyNotes]:
    # specify the file and the directory to work in
    src_filepath: Path = Path("tests/week_2_files/Test Week 2.md")

    # copy the weekly file to test directory
    dst_filepath: Path = temp_dir / src_filepath.name
    shutil.copy(src_filepath, dst_filepath)

    week_2_notes: WeeklyNotes = load_weekly_note_file(file=dst_filepath)
    yield week_2_notes
