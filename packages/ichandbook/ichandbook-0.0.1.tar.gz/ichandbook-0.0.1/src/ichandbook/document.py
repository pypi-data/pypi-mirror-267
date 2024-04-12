import logging
from pathlib import Path

from .markdown_page import MarkdownPage
from .link_validator import LinkValidator

logger = logging.getLogger(__name__)


class Document:
    def __init__(self, root: Path, content_dir: Path) -> None:
        self.root = root
        self.link_validator = LinkValidator()
        self.pages: list = []

        logger.info(f"Looking for pages in {self.root / content_dir}")
        self.load_pages(self.root)
        logger.info(f"Found {len(self.pages)} pages")

    def load_pages(self, path: Path):
        for direntry in path.iterdir():
            if direntry.is_file() and direntry.suffix == ".md":
                relative_path = direntry.relative_to(self.root)
                self.pages.append(MarkdownPage(self.root, relative_path))
            elif direntry.is_dir():
                self.load_pages(direntry)

    def validate_links(self):
        self.link_validator.validate_links(self.pages)
