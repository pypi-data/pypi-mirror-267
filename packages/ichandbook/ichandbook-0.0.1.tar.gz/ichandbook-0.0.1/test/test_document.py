from pathlib import Path
from ichandbook.document import Document


def get_test_data_dir():
    return Path(__file__).parent / "data"


def test_document():
    content_root = get_test_data_dir() / "mock_document"
    doc = Document(content_root, Path())
    doc.validate_links()
