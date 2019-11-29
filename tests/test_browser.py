import os
import unittest
import inspect

from deepl_scraper.browser import Browser

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


class BrowserTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        """Override TestCase's __init__ and let the base class handle the arguments."""
        super(BrowserTest, self).__init__(*args, **kwargs)
        self.WEBDRIVERS_DIR = os.path.join(ROOT_DIR, "src", "deepl_scraper", 'webdrivers')

    def test_1_does_webdrivers_directory_exist(self):
        print(f"Running Test Method : {inspect.stack()[0][3]}")
        error_message = f"No 'webdrivers' directory under {self.WEBDRIVERS_DIR}"
        self.assertTrue(os.path.exists(self.WEBDRIVERS_DIR), error_message)

    def test_2_is_selenium_binary_downlaoded(self):
        print(f"Running Test Method : {inspect.stack()[0][3]}")
        error_message = f"No selenium driver-binary under {self.WEBDRIVERS_DIR}. Download it from seleniumhq.org"
        binary_files = os.listdir(self.WEBDRIVERS_DIR)
        self.assertNotEqual(len(binary_files), 0, error_message)

    def test_3_does_browser_start(self):
        print(f"Running Test Method : {inspect.stack()[0][3]}")
        self.browser = Browser(headless=True)
        self.browser.driver.quit()


if __name__ == '__main__':
    unittest.main(verbosity=3)
