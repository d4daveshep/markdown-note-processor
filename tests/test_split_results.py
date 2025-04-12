from md_parser import NoteSummary, ProjectFileDetails, SplitResults


def test_create_empty_split_results() -> None:
    results: SplitResults = SplitResults()
    assert results


def test_increment_lines_processed() -> None:
    results: SplitResults = SplitResults()
    assert results.lines_procesed == 0
    results.lines_procesed += 1
    assert results.lines_procesed == 1


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


def test_note_summary_entries() -> None:
    pfd: ProjectFileDetails = ProjectFileDetails(name="Project 1")
    assert len(pfd.entries) == 0

    note_summary: NoteSummary = NoteSummary(
        title="My first note", date_str="Wed 1 Jan 2025"
    )
    assert note_summary.lines_written == 0
    pfd.entries.append(note_summary)
    assert len(pfd.entries) == 1

    note_summary.lines_written += 1
    assert note_summary.lines_written == 1
