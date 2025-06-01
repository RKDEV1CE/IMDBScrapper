import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Add project root to sys.path so we can import master_scrapper
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from master_scrapper import scrape_keyword
class TestMasterScraper(unittest.TestCase):
    @patch('master_scrapper.webdriver.Chrome')
    @patch('master_scrapper.WebDriverWait')
    def test_scrape_keyword_basic(self, mock_webdriverwait, mock_chrome):
        # Setup mock driver and mock WebDriverWait
        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver
        mock_wait = MagicMock()
        mock_webdriverwait.return_value = mock_wait

        # Mock button element for clicking
        mock_button = MagicMock()
        mock_wait.until.return_value = mock_button

        # Mock list items found by driver.find_elements
        mock_element = MagicMock()
        # Mock anchor tag inside the li
        mock_anchor = MagicMock()
        mock_anchor.text = "Test Movie"
        mock_anchor.get_attribute.return_value = "http://example.com"
        mock_element.find_element.return_value = mock_anchor
        # Mock the text lines to simulate year and cast
        mock_element.text = "Test Movie\n2023\nSome Cast"

        mock_driver.find_elements.return_value = [mock_element]

        # Call your function (you can choose any keyword and iteration count)
        scrape_keyword("Action", 1)

        # Assert driver was started and quit
        mock_chrome.assert_called_once()
        mock_driver.quit.assert_called_once()

        # Assert button was clicked
        mock_button.click.assert_called()

        # Assert find_elements was called to get results
        mock_driver.find_elements.assert_called()

if __name__ == "__main__":
    unittest.main()
