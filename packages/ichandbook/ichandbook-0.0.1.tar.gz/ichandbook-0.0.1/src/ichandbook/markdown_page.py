from pathlib import Path
import markdown
from bs4 import BeautifulSoup


class MarkdownPage:
    def __init__(self, doc_root: Path, file_path: Path) -> None:
        self.doc_root = doc_root
        self.file_path = file_path
        self.md = None
        self.html = None
        self.soup = None
        self.links: list = []
        self.load()

    def get_full_path(self):
        return self.doc_root / self.file_path

    def load(self):
        with open(self.get_full_path(), "r") as f:
            self.md = f.read()
        self.html = markdown.markdown(self.md)
        self.soup = BeautifulSoup(self.html, features="html.parser")
        self.links = self.soup.find_all("a", href=True)
