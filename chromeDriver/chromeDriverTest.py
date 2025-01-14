import json
import unittest
import urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os
from chromeDriver import ConfigureChromeDriver

class TestConnection(unittest.TestCase):
    def setUp(self):
        # Load configuration
        self.config_file_path = "../jobApp/secrets/config.json"

    def test_chromedriver_connection(self):
        print("Testing ChromeDriver connection and website access")
        try:
            self.driver = ConfigureChromeDriver(self.config_file_path).driver
            self.driver.get("https://www.google.com")
            expected_title = "Google"
            actual_title = self.driver.title
            self.assertEqual(actual_title, expected_title,
                             f"Expected title: {expected_title}, Actual title: {actual_title}")
        finally:
            # Close the browser window, regardless of whether the test passed or failed.
            if self.driver:
                self.driver.quit()


if __name__ == '__main__':
    unittest.main()
