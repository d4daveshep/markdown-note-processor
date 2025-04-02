import shutil
from pathlib import Path


def test_split_first_weekly_file() -> None:
    # specify the file and the directory to work in
    src_md_filepath: Path = Path("tests/Test Week 1.md")

    # create the test directory
    test_dir: Path = Path("./temp_test")
    test_dir.mkdir(exist_ok=True)

    # delete all files in test directory
    file_path: Path
    for file_path in test_dir.glob("*"):
        if file_path.is_file():
            file_path.unlink()

    # copy the weekly file to test directory
    md_filepath: Path = test_dir / src_md_filepath.name
    shutil.copy(src_md_filepath, md_filepath)

    # parse the file
    # md_parser: MDParser = MDParser(md_filepath)

    # check the file structure

    # split the file

    # check the correct files are created

    # check the contents of the files matches expected contents

    pass


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
