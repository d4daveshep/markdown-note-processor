# Parsing rules

First line must be H1 with format # Wnn yyyy: <date range> (but we don't care about the <date range>), store H1.date_str as Wnn yyyy

For each H1:

- With format "# ddd dd mmm yyyy", store this date as H1.date_str
- With a different format, store H1.date_str as Wnn yyyy
- Close existing H2.project_name file if one is open

For each H2:

- Close existing H2.project_name file if one is open
- Store text up to before hyphen as H2.project_name and text after the hyphen as H2.tile. If no hyphen then store text to end of line as H2.project_name and H2.title is "".
- Open file H2.project_name for appending, or create file if doesn't exist.
- Append as H1 heading: H1.date_str: H2.title

Append each other line (not H1 or H2), including blank lines, lists, H3 and lower headings to H2.project_name file
