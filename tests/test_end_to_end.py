import filecmp
from pathlib import Path

from md_parser import NoteFile, SplitResults


def test_split_first_weekly_file(week_1: NoteFile, temp_dir: Path) -> None:
    results: SplitResults = week_1.split_file()

    # check project files are created and are written as expected
    project_files: list[str] = [f"Project {n}.md" for n in range(0, 3)]
    for file in project_files:
        assert Path(temp_dir / file).exists(), f"{file} not found"
        assert filecmp.cmp(Path(f"./tests/{file}"), Path(temp_dir / file)), (
            f"{file} differs"
        )

    assert results.lines_procesed == 54


def test_split_second_weekly_file() -> None:
    # specify the file and the directory to work in

    # copy the file to the directory

    # parse the file

    # check the file structure

    # split the file

    # check the correct files are created or updated

    # check the contents of the files matches expected contents

    # delete the directory
    pass
