"""Offline checks for the book's purchase call to action.

Run with: python -m unittest discover -s tests -v
"""

from html.parser import HTMLParser
from pathlib import Path
import unittest
from urllib.parse import urlsplit


class PageParser(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.links = []
        self.text = []
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.links.append(dict(attrs).get("href", ""))

    def handle_data(self, data):
        self.text.append(data)


class PurchaseCTATests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        source = Path(__file__).resolve().parents[1] / "index.html"
        cls.page = PageParser(source.read_text(encoding="utf-8"))

    def test_no_placeholder_purchase_destination(self):
        for href in self.page.links:
            with self.subTest(href=href):
                self.assertNotIn("placeholder", urlsplit(href).path.lower())

    def test_publication_note_remains_visible_text(self):
        self.assertIn(
            "Link goes live on publication day — check back soon.",
            "".join(self.page.text),
        )


if __name__ == "__main__":
    unittest.main()
