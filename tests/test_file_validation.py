from md_parser import NoteFile


def test_first_h1_is_weekly_format():
    good_h1: str = "# W12 2025: 3 Nov - 9 Nov"
    assert NoteFile.validate_weekly_heading(good_h1)
