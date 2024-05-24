# -*- coding: utf-8 -*-

import os
import unittest

import tmx_products.tmx_projectconfig


class TestStringExtraction(unittest.TestCase):
    def setUp(self):
        self.testfiles_path = os.path.join(os.path.dirname(__file__), "testfiles")
        self.storage_path = os.path.join(self.testfiles_path, "output_android")

    def testGetAndroidStringsGerman(self):
        toml_path = os.path.join(self.testfiles_path, "android", "l10n.toml")
        extraction = tmx_products.tmx_projectconfig.StringExtraction(
            toml_path, self.storage_path, "en-US", "test"
        )
        extraction.extractStrings()

        strings_locale = extraction.translations
        self.assertEqual(len(strings_locale), 11)
        self.assertEqual(len(strings_locale["it"]), 4)
        self.assertEqual(len(strings_locale["en-US"]), 17)
        self.assertEqual(len(strings_locale["es-ES"]), 5)


if __name__ == "__main__":
    unittest.main()
