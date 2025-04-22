import filecmp
from pathlib import Path

from md_parser import NoteFile, SplitResults


def test_split_first_weekly_file(week_1: NoteFile, temp_dir: Path) -> None:
    results: SplitResults = week_1.split_file()
    assert results.lines_processed == 54

    # check project files are created and are written as expected
    project_files: list[str] = [f"Project {n}.md" for n in range(0, 4)]
    for file in project_files:
        assert Path(temp_dir / file).exists(), f"{file} not found"
        assert filecmp.cmp(
            Path(f"./tests/week_1_files/{file}"), Path(temp_dir / file)
        ), f"{file} differs"


def test_split_file_dry_run(week_1: NoteFile, temp_dir: Path) -> None:
    week_1.dry_run = True
    week_1.split_file()

    # check project files are NOT created
    project_files: list[str] = [f"Project {n}.md" for n in range(0, 4)]
    for file in project_files:
        assert not Path(temp_dir / file).exists(), f"{file} was found"


def test_split_second_weekly_file(
    week_1: NoteFile, week_2: NoteFile, temp_dir: Path
) -> None:
    week_1.split_file()
    results: SplitResults = week_2.split_file()
    assert results.lines_processed == 38

    # check project files existand are written as expected
    project_files: list[str] = [f"Project {n}.md" for n in range(0, 5)]
    for file in project_files:
        assert Path(temp_dir / file).exists(), f"{file} not found"
        assert filecmp.cmp(
            Path(f"./tests/week_2_files/{file}"), Path(temp_dir / file)
        ), f"{file} differs"

    assert False, (
        "add some test functionality here,  e.g. are the files correct?  which got amended vs created"
    )
