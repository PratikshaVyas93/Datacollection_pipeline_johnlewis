# import the unittestcase
import unittest
# import sys to allow us to append the system path
import sys
# append the parent folder
sys.path.append('../') 
sys.path.insert(0, '../src')
from src.scraper import *
from unittest.mock import patch, MagicMock

class ScraperTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.scraper = Scraper()

    @patch('urllib.request.urlretrieve')
    def test_download_images(self, mock_urlretrieve):
        mock_urlretrieve.return_value = MagicMock()
        self.scraper.download_images('test-images_folder_path', 'test-product_image_link', 'test-product_id')
        mock_urlretrieve.assert_called_once_with('test-product_image_link', 'test-images_folder_path/test-product_id.jpg')

    def test_get_product_information(self):
        self.scraper.load_page('https://www.johnlewis.com')

        self.actual_product_list = self.scraper.get_product_information()
        self.assertEqual(list, type(self.actual_product_list))

    def tearDown(self) -> None:
        self.scraper.driver.close()

if __name__ == "__main__":
    unittest.main(argv=[''], verbosity=0, exit=False)