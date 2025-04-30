# Testing the SplitResults class
from split_results import ProjectFileDetails, SplitResults, TitleDate


def test_create_empty_split_results() -> None:
    results: SplitResults = SplitResults()
    assert results
    assert results.total_lines_written == 0


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

    pfd.lines_written[TitleDate(title="Title", date_str="Date")] = 0
    pfd.lines_written[TitleDate(title="Title", date_str="Date")] += 1
    assert pfd.lines_written[TitleDate(title="Title", date_str="Date")] == 1


def test_merge_new_project_file_details() -> None:
    results: SplitResults = SplitResults()
    pfd_1: ProjectFileDetails = ProjectFileDetails(name="Project 1")
    pfd_1.created = True
    td_1 = TitleDate(title="Title 1", date_str="Date 1")
    pfd_1.lines_written[td_1] = 11
    results.projects[pfd_1.name] = pfd_1

    pfd_2: ProjectFileDetails = ProjectFileDetails(name="Project 2")
    td_2 = TitleDate(title="Title 2", date_str="Date 2")
    pfd_2.lines_written[td_2] = 22
    pfd_2.created = False

    results.merge_project_file_details(pfd_2)
    assert results.total_lines_written == 33

    # check pfd_1 is still there
    assert pfd_1.name in results.projects
    assert td_1 in results.projects[pfd_1.name].lines_written
    assert results.projects[pfd_1.name].created

    # check pfd_2 has been merged
    assert len(results.projects) == 2
    assert pfd_2.name in results.projects
    assert td_2 in results.projects[pfd_2.name].lines_written
    assert not results.projects[pfd_2.name].created

    # check pfd_1 is still there
    assert pfd_1.name in results.projects
    assert td_1 in results.projects[pfd_1.name].lines_written
    assert results.projects[pfd_1.name].created


def test_merge_existing_project_file_details() -> None:
    results: SplitResults = SplitResults()
    pfd_1: ProjectFileDetails = ProjectFileDetails(name="Project 1")
    pfd_1.created = True
    td_1 = TitleDate(title="Title 1", date_str="Date 1")
    pfd_1.lines_written[td_1] = 11
    results.projects[pfd_1.name] = pfd_1

    pfd_2: ProjectFileDetails = ProjectFileDetails(name="Project 1")
    pfd_2.created = False
    td_2 = TitleDate(title="Title 2", date_str="Date 2")
    pfd_2.lines_written[td_2] = 22

    results.merge_project_file_details(pfd_2)
    assert results.total_lines_written == 33

    assert pfd_1.name in results.projects
    assert td_1 in results.projects[pfd_1.name].lines_written
    assert results.projects[pfd_1.name].created

    # check pfd_2 has been merged
    assert len(results.projects) == 1
    assert pfd_2.name in results.projects
    assert td_2 in results.projects[pfd_2.name].lines_written


def test_merge_existing_project_file_and_title_date_details() -> None:
    results: SplitResults = SplitResults()
    pfd_1: ProjectFileDetails = ProjectFileDetails(name="Project 1")
    pfd_1.created = True
    td_1 = TitleDate(title="Title 1", date_str="Date 1")
    pfd_1.lines_written[td_1] = 11
    results.projects[pfd_1.name] = pfd_1

    pfd_2: ProjectFileDetails = ProjectFileDetails(name="Project 1")
    pfd_2.created = False
    pfd_2.lines_written[td_1] = 11

    results.merge_project_file_details(pfd_2)
    assert results.total_lines_written == 22

    assert pfd_1.name in results.projects
    assert td_1 in results.projects[pfd_1.name].lines_written
    assert results.projects[pfd_1.name].created

    assert results.projects[pfd_1.name].lines_written[td_1] == 22
    assert results.projects[pfd_1.name].created
