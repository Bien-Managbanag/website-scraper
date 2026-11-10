import unittest
from scrapy.http import HtmlResponse, Request
from books.items import BooksItem
from books.spiders.book import BookSpider
from pathlib import Path

class BookSpiderTest(unittest.TestCase):
    def setUp(self):
        self.spider = BookSpider()
        html_path = Path(__file__).parent / "sample.html"
        self.example_html = html_path.read_text(encoding="utf-8")

        # Create a simulated Scrapy response
        self.response = HtmlResponse(
            url="https://books.toscrape.com/",
            body=self.example_html.encode("utf-8"),
            encoding="utf-8"
        )

        self.response = HtmlResponse(
            url="https://books.toscrape.com",
            body=self.example_html,
            encoding="utf-8"
        )

    #Test if the spider scrapes books and pagination links
    def test_parse_scrapes_all_items(self):
        """Test if the spider scrapes all books and pagination links."""
        # Collect the items produced by the generator in a list
        # so that it's possible to iterate over it more than once.
        results = list(self.spider.parse(self.response))

        # There should be two book items and one pagination request
        book_items = [item for item in results if isinstance(item, BooksItem)]
        pagination_requests = [
            item for item in results if isinstance(item, Request)
        ]

        self.assertEqual(len(book_items), 2)
        self.assertEqual(len(pagination_requests), 1)

    #Test if the spider scrapes the correct information for each book
    def test_parse_scrapes_correct_book_information(self):
        results_generator = self.spider.parse(self.response)

        # Book 1
        book_1 = next(results_generator)
        self.assertEqual(
            book_1["url"], "catalogue/a-light-in-the-attic_1000/index.html"
        )
        self.assertEqual(book_1["title"], "A Light in the Attic")
        self.assertEqual(book_1["price"], "£51.77")

        # Book 2
        book_2 = next(results_generator)
        self.assertEqual(
            book_2["url"], "catalogue/tipping-the-velvet_999/index.html"
        )
        self.assertEqual(book_2["title"], "Tipping the Velvet")
        self.assertEqual(book_2["price"], "£53.74")

    #Test if the spider creates a pagination request correctly
    def test_parse_scrapes_creates_pagination_request(self):
        results = list(self.spider.parse(self.response))
        next_page_request = results[-1]
        self.assertIsInstance(next_page_request, Request)
        self.assertEqual(
            next_page_request.url,
            "https://books.toscrape.com/catalogue/page-2.html",
        )

if __name__ == "__main__":
    unittest.main()