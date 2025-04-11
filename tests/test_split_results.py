from md_parser import ProjectFileDetails, SplitResults


def test_create_empty_split_results():
    results: SplitResults = SplitResults()
    assert results


def test_increment_lines_processed():
    results: SplitResults = SplitResults()
    assert results.lines_procesed == 0
    results.lines_procesed += 1
    assert results.lines_procesed == 1


def test_project_file_created_appended_flag():
    results: SplitResults = SplitResults()
    project_name: str = "Project 1"
    # date_str: str = "Mon 12 Apr 2025"
    project: ProjectFileDetails = ProjectFileDetails(name=project_name)
    results.projects[project_name] = project

    project: ProjectFileDetails = results.projects[project_name]

    assert project.name == project_name
    # assert project.date_str == date_str
    assert not project.created
