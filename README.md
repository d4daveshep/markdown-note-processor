# Project File Writer

## About

This is a utility for splitting my weekly markdown notes file into separate project files. Often I'm working on long-running projects so the project files are appended to over many weeks.

Sometimes I work on the same project multiple times through the taking notes in different sections of the weekly notes file, but with the same date and title. These should also be appended to the project notes.

Finally I may want to run this utility multiple times during the week so the utility needs to detect if the notes already exist in the project file and skip them if they do.

## Usage

Use a modern version of python and there are no external dependencies.

#### Running the file

`python project_file_writer [options] notes_file_name.md`

#### Options

`-o --output_dir <output directory>` default is the same directory as the weekly notes file

`-s --dry-run` Simulates the process but doesn't actually create or write to any files

`-d --debug` Output debugging information

## Weekly notes markdown format rules

1. The first line must contain a H1 heading with the week number and date range in the following format:

   - `# Week nn yyyy: dd - dd mmm` For example: `# Week 18 2025: 28 Apr - 4 May`

2. Any plain text lines after the week heading are ignored.

3. Each day section must use a H1 heading in the following format:

   - `# ddd dd mmm yyyy` For example: `# Tue 29 Apr 2025`

4. Project names and titles use a H2 heading in the following format:

   - `## <project name> - <note title or subject>` For example: `## My Project - Note Subject`
   - the note title or subject is optional, for example `## My Project`

5. Any H1 headings not in the correct day format will be ignored along with any headings or plain text lines following them (until a valid day H2 heading)

6. Any H3 or lower headings and any plain text lines within a H2 project name/title heading are copied the corresponding project note

## Project notes markdown format rules

1. The first line in a project note file contains a H1 heading with the project name. This is taken from the H2 project title using the text before the first hyphen.

   - for example the H2 heading in a weekly note file `## My Project Name - My note title - first draft` would result in a project file called `My Project Name.md` with the H1 heading `# My Project Name``

2. Each project note in the file uses a H2 heading containing the date of note (taken from the weekly notes day (or week) headings. For example:

   - `## Tue 29 Apr 2025: Note title - first draft`

3. Any H3 or lower headings and any plain text lines including blank lines are copied as is from the weekly notes file to the project file.

## Processing diagram

[ image placeholder ]
