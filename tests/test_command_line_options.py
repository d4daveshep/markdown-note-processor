from md_parser import CommandLineArguments, parse_args


def test_dry_run_argument() -> None:
    args: CommandLineArguments = parse_args(["file.md", "--dry-run"])
    assert args.filename == "file.md"
    assert args.dry_run
    assert not args.debug
