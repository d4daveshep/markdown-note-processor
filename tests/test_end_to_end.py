import filecmp
from projectfile_writer import write_project_files
from pathlib import Path

from md_parser import SplitResults
from weekly_notes import WeeklyNotes


def test_split_first_weekly_file(week_1_notes: WeeklyNotes, temp_dir: Path) -> None:
    results: SplitResults = write_project_files(week_1_notes, temp_dir)
    assert results.total_lines_written == 34
    # print(f"total_lines_written={results.total_lines_written}")

    # check project files are created and are written as expected
    project_files: list[str] = [f"Project {n}.md" for n in range(0, 4)]
    for file in project_files:
        assert Path(temp_dir / file).exists(), f"{file} not found"
        assert filecmp.cmp(
            Path(f"./tests/week_1_files/{file}"), Path(temp_dir / file)
        ), f"{file} differs"


def test_split_file_dry_run(week_1_notes: WeeklyNotes, temp_dir: Path) -> None:
    write_project_files(week_1_notes, temp_dir, dry_run=True)

    # check project files are NOT created
    project_files: list[str] = [f"Project {n}.md" for n in range(0, 4)]
    for file in project_files:
        assert not Path(temp_dir / file).exists(), f"{file} was found"


def test_split_second_weekly_file(
    week_1_notes: WeeklyNotes, week_2_notes: WeeklyNotes, temp_dir: Path
) -> None:
    write_project_files(week_1_notes, temp_dir)
    results: SplitResults = write_project_files(week_2_notes, temp_dir)
    assert results.total_lines_written == 24

    # check project files exist and are written as expected
    project_files: list[str] = [f"Project {n}.md" for n in range(0, 5)]
    for file in project_files:
        assert Path(temp_dir / file).exists(), f"{file} not found"
        assert filecmp.cmp(
            Path(f"./tests/week_2_files/{file}"), Path(temp_dir / file)
        ), f"{file} differs"


def test_rerun_of_weekly_file_split(week_1_notes: WeeklyNotes, temp_dir: Path) -> None:
    write_project_files(week_1_notes, temp_dir)
    write_project_files(week_1_notes, temp_dir)

    # check project files are created but content not duplicated on second split
    project_files: list[str] = [f"Project {n}.md" for n in range(0, 4)]
    for file in project_files:
        assert Path(temp_dir / file).exists(), f"{file} not found"
        assert filecmp.cmp(
            Path(f"./tests/week_1_files/{file}"), Path(temp_dir / file)
        ), f"{file} differs"
