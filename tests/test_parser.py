from pathlib import Path


def test_load_file():
    md_filepath: Path = Path("Test Week 1.md")
    assert md_filepath.exists()
