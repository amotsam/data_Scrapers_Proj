import unittest
from scripts.scrapers.testDomainScraper import parse_data

class TestScraperParseData(unittest.TestCase):
    def test_parse_data(self):
        html = """
        <html>
            <body>
                <div class="item">
                    <h2>Item 1</h2>
                    <span class="price">$10</span>
                </div>
                <div class="item">
                    <h2>Item 2</h2>
                    <span class="price">$20</span>
                </div>
            </body>
        </html>
        """
        expected_output = [
            {"title": "Item 1", "price": "$10"},
            {"title": "Item 2", "price": "$20"},
        ]

        result = parse_data(html)
        self.assertEqual(result, expected_output)

    def test_parse_data_empty(self):
        html = "<html><body></body></html>"
        result = parse_data(html)
        self.assertEqual(result, [])

if __name__ == "__main__":
    unittest.main()
