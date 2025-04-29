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
    lines_processed: int = 0
    week_num: str = ""
    top_heading: str = ""
    projects: dict[str, ProjectFileDetails] = field(
        default_factory=dict[str, ProjectFileDetails]
    )
    days: set[str] = field(default_factory=set[str])

    def merge_project_file_details(
        self, new_project_file_details: ProjectFileDetails
    ) -> None:
        pass

    def __str__(self) -> str:
        output = ""
        output += "\n======== Split Results ========\n"
        output += self.top_heading
        output += "\n-------------------------------\n"
        output += f"Processed {self.lines_processed} lines\n"

        output += "Project files written to:\n"
        for project_name, details in sorted(self.projects.items()):
            output += f"- {project_name}\t"
            if details.created:
                output += "[ CREATED ]\n"
            else:
                output += "[ exists ]\n"
        output += "-------------------------------\n"

        output += "\nNotes entries written:\n"
        for project_name, details in sorted(self.projects.items()):
            output += f"\nProject file: {project_name}:\n"
            for title_date, lines in details.lines_written.items():
                output += f'On {title_date[1]}, topic "{title_date[0]}", wrote {lines} lines\n'
        output += "-------------------------------\n"

        return output
