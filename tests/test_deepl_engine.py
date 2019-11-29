import unittest

from deepl_scraper.translator import DeepLEngine


class TestDeepL(unittest.TestCase):

    def test_translation(self):
        self.deepl = DeepLEngine('en', 'de')
        translation = self.deepl.translate("hello, world!")
        print(translation)
        self.assertEqual("Hallo, Welt!", translation)


if __name__ == '__main__':
    unittest.main(verbosity=3)
