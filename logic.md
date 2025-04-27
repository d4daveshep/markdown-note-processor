## Processing a H2 heading

### Purpose

To open (get or create) a project file to write the lines following the H2 heading to.

But if the project file already contains the same note title on the same date then we should ignore following lines because we've already split the weekly notes file.

### Logic

1. extract the project name and note title from the H2 heading
2. if we don't have a date, then use the week number as the date
3. build the title line from the date and note title
4. using the project name, get/create a project details record from the results object
5. if the project file already exists and does NOT contain the title line, then
   - open the project file
6. if the project file already exists and does CONTAIN the title line then,
   - set the project name to "" so that subsequent lines are ignored
7. if the project file doesn't exist then,
   - create project file
   - write the project name as a H1 heading in the file
   - set the created flag in the project details record to true
8. if we still have a project name (i.e. not ""), then
   - write the title line to the project file
   - update the project file details with the title, and
   - set the lines written to 0
