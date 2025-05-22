# -*- coding: utf-8 -*-

import os
import unittest

import tmx_products.tmx_projectconfig


class TestStringExtraction(unittest.TestCase):
    def setUp(self):
        self.testfiles_path = os.path.join(os.path.dirname(__file__), "testfiles")
        self.storage_path = os.path.join(self.testfiles_path, "output_android")

    def testGetAndroidStrings(self):
        toml_path = os.path.join(self.testfiles_path, "android", "l10n.toml")
        extraction = tmx_products.tmx_projectconfig.StringExtraction(
            toml_path, self.storage_path, "en-US", "test", True
        )
        extraction.extractStrings()

        strings_locale = extraction.translations
        self.assertEqual(len(strings_locale), 11)
        self.assertEqual(len(strings_locale["it"]), 6)
        self.assertEqual(len(strings_locale["en-US"]), 17)
        self.assertEqual(len(strings_locale["es-ES"]), 5)

        # Check escapes
        self.assertEqual(
            strings_locale["it"][
                "test/mozilla-lockwise/lockwise-android/app/src/main/res/values/strings.xml:escaped_quote"
            ],
            "Sblocca comodamente l'app utilizzando la tua impronta digitale",
        )
        self.assertEqual(
            strings_locale["it"][
                "test/mozilla-lockwise/lockwise-android/app/src/main/res/values/strings.xml:escaped_doublequote"
            ],
            'Sblocca comodamente l’app utilizzando la tua "impronta digitale"',
        )

    def testGetProductStrings(self):
        toml_path = os.path.join(self.testfiles_path, "toml", "l10n.toml")
        extraction = tmx_products.tmx_projectconfig.StringExtraction(
            toml_path, self.storage_path, "en", "test", False
        )
        extraction.extractStrings()

        strings_locale = extraction.translations
        self.assertEqual(len(strings_locale), 4)
        self.assertEqual(len(strings_locale["it"]), 1)
        self.assertEqual(len(strings_locale["en"]), 2)
        self.assertEqual(len(strings_locale["de"]), 2)
        self.assertEqual(len(strings_locale["fr"]), 0)


if __name__ == "__main__":
    unittest.main()
