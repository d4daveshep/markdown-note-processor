from md_parser import NoteFile


def test_first_h1_is_weekly_format():
    valid_h1: list[str] = [
        "# W01 2023: This is a valid string",
        "# W52 2024: Another valid string",
    ]
    for heading in valid_h1:
        assert NoteFile.validate_weekly_heading(heading)

    invalid_h1: list[str] = [
        "# W00 2023: Invalid - week number out of range",
        "# W53 2023: Invalid - week number out of range",
        "# W12 23: Invalid - year isn't 4 digits",
        " # W12 2023: Invalid - doesn't start at beginning of string",
        "# w12 2023: Invalid - 'W' must be uppercase",
    ]
    for heading in invalid_h1:
        assert not NoteFile.validate_weekly_heading(heading)
