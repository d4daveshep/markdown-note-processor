from project_file_writer import CommandLineArguments, parse_args


def test_dry_run_argument() -> None:
    args: CommandLineArguments = parse_args(
        ["file.md", "-o", "temp/", "--dry-run", "-v"]
    )
    assert args.filename == "file.md"
    assert args.output_dir == "temp/"
    assert args.dry_run
    assert args.verbose
    assert not args.debug
