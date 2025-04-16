from md_parser import ProjectFileDetails, SplitResults


def test_create_empty_split_results() -> None:
    results: SplitResults = SplitResults()
    assert results


def test_increment_lines_processed() -> None:
    results: SplitResults = SplitResults()
    assert results.lines_processed == 0
    results.lines_processed += 1
    assert results.lines_processed == 1


def test_project_file_created_appended_flag() -> None:
    results: SplitResults = SplitResults()
    project_name: str = "Project 1"
    project: ProjectFileDetails = ProjectFileDetails(name=project_name)
    results.projects[project_name] = project

    project = results.projects[project_name]

    assert project.name == project_name
    assert not project.created


def test_profile_file_details() -> None:
    pfd: ProjectFileDetails = ProjectFileDetails(name="Project 1")
    assert not pfd.created


def test_project_lines_written() -> None:
    pfd: ProjectFileDetails = ProjectFileDetails(name="Project 1")
    assert len(pfd.lines_written) == 0

    pfd.lines_written[("Title", "Date")] = 0
    pfd.lines_written[("Title", "Date")] += 1
    assert pfd.lines_written[("Title", "Date")] == 1
