# Testing the SplitResults class
from md_parser import ProjectFileDetails, SplitResults, TitleDate


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

    pfd.lines_written[TitleDate(title="Title", date_str="Date")] = 0
    pfd.lines_written[TitleDate(title="Title", date_str="Date")] += 1
    assert pfd.lines_written[TitleDate(title="Title", date_str="Date")] == 1


def test_merge_new_project_file_details() -> None:
    results: SplitResults = SplitResults()
    pfd_1: ProjectFileDetails = ProjectFileDetails(name="Project 1")
    pfd_1.lines_written[TitleDate(title="Title 1", date_str="Date 1")] = 11
    results.projects[pfd_1.name] = pfd_1

    pfd_2: ProjectFileDetails = ProjectFileDetails(name="Project 2")
    pfd_2.lines_written[TitleDate(title="Title 2", date_str="Date 2")] = 22

    results.merge_project_file_details(pfd_2)

    # check pfd_1 is still there
    assert pfd_1.name in results.projects
    assert (
        TitleDate(title="Title 1", date_str="Date 1")
        in results.projects[pfd_1.name].lines_written
    )

    # check pfd_2 has been merged
    assert len(results.projects) == 2
    assert pfd_2.name in results.projects
    assert (
        TitleDate(title="Title 2", date_str="Date 2")
        in results.projects[pfd_2.name].lines_written
    )

    # check pfd_1 is still there
    assert pfd_1.name in results.projects
    assert (
        TitleDate(title="Title 1", date_str="Date 1")
        in results.projects[pfd_1.name].lines_written
    )


def test_merge_existing_project_file_details() -> None:
    results: SplitResults = SplitResults()
    pfd_1: ProjectFileDetails = ProjectFileDetails(name="Project 1")
    pfd_1.lines_written[TitleDate(title="Title 1", date_str="Date 1")] = 11
    results.projects[pfd_1.name] = pfd_1

    pfd_2: ProjectFileDetails = ProjectFileDetails(name="Project 1")
    pfd_2.lines_written[TitleDate(title="Title 2", date_str="Date 2")] = 22

    results.merge_project_file_details(pfd_2)

    assert pfd_1.name in results.projects
    assert (
        TitleDate(title="Title 1", date_str="Date 1")
        in results.projects[pfd_1.name].lines_written
    )

    # check pfd_2 has been merged
    assert len(results.projects) == 1
    assert pfd_2.name in results.projects
    assert (
        TitleDate(title="Title 2", date_str="Date 2")
        in results.projects[pfd_2.name].lines_written
    )
