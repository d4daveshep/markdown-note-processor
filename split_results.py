from dataclasses import dataclass, field
from typing import NamedTuple


class TitleDate(NamedTuple):
    title: str = ""
    date_str: str = ""


@dataclass
class ProjectFileDetails:
    name: str
    created: bool = False
    lines_written: dict[TitleDate, int] = field(default_factory=dict[TitleDate, int])


@dataclass
class SplitResults:
    week_num: str = ""
    top_heading: str = ""
    projects: dict[str, ProjectFileDetails] = field(
        default_factory=dict[str, ProjectFileDetails]
    )
    days: set[str] = field(default_factory=set[str])

    @property
    def total_lines_written(self) -> int:
        total: int = 0
        for details in self.projects.values():
            total += sum(details.lines_written.values())
        return total

    def merge_project_file_details(self, new_details: ProjectFileDetails) -> None:
        # find or create the project in the results
        details: ProjectFileDetails = self.projects.get(
            new_details.name, ProjectFileDetails(name=new_details.name)
        )

        # if created flag is True then don't override it with False
        if new_details.created:
            details.created = True

        for title_date, line_count in new_details.lines_written.items():
            # get the existing line count if it exists (or use 0)
            existing_line_count: int = details.lines_written.get(title_date, 0)

            details.lines_written[title_date] = existing_line_count + line_count

        self.projects[new_details.name] = details

        pass

    def summary_output(self) -> str:
        output = ""
        output += "\n======== Split Results Summary ========\n"
        output += self.top_heading
        output += "\n---------------------------------------\n"
        output += f"Total lines written = {self.total_lines_written}\n"

        output += "Project files written to:\n"
        for project_name, details in sorted(self.projects.items()):
            output += f"- {project_name}\t"
            if details.created:
                output += "[ CREATED ]\n"
            else:
                output += "[ exists ]\n"
        output += "---------------------------------------\n"
        return output

    def detailed_output(self) -> str:
        output = ""
        output += "======== Split Results Details ========\n"
        output += "\nNotes entries written:\n"
        for project_name, details in sorted(self.projects.items()):
            output += f"\nProject file: {project_name}:\n"
            for title_date, lines in details.lines_written.items():
                output += f'On {title_date[1]}, topic "{title_date[0]}", wrote {lines} lines\n'
        output += "---------------------------------------\n"
        return output

    def __str__(self) -> str:
        output = self.summary_output() + self.detailed_output()
        return output
