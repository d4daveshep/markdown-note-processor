from pathlib import Path

from markdown_it import MarkdownIt

md = MarkdownIt()
md_filepath: Path = Path("tests/Test Week 1.md")
if __name__ == "__main__":
    with open(md_filepath, "r") as file:
        data: str = file.read()
        for token in md.parse(data):
            print(token)
            print()
