# -*- coding: utf-8 -*-

import filecmp
import os
import unittest

import tmx_repository as tmx_prod


class TestStringExtraction(unittest.TestCase):
    def setUp(self):
        self.testfiles_path = os.path.join(os.path.dirname(__file__), "testfiles")
        self.storage_path = os.path.join(self.testfiles_path, "output")

    def testGetProductStringsChinese(self):
        repo_path = os.path.join(self.testfiles_path, "product", "zh-CN")
        extraction = tmx_prod.StringExtraction(
            self.storage_path, "zh-CN", "en-US", "test"
        )
        extraction.setRepositoryPath(repo_path)
        extraction.extractStrings()

        strings_locale = extraction.translations
        self.assertEqual(len(strings_locale), 27)
        self.assertTrue(
            "browser/branding/official/brand.dtd:brandFullName" in strings_locale
        )
        self.assertTrue(
            "browser/branding/official/brand.properties:brandShortName"
            in strings_locale
        )
        self.assertTrue("browser/defines.inc:MOZ_LANGPACK_CREATOR" in strings_locale)
        self.assertTrue("dom/chrome/appstrings.properties:zeroTest" in strings_locale)
        self.assertEqual(
            strings_locale["dom/chrome/appstrings.properties:zeroTest"], "0"
        )

        self.assertEqual(
            strings_locale[
                "browser/chrome/browser/taskbar.properties:taskbar.tasks.newWindow.label"
            ],
            "打开新窗口",
        )
        self.assertEqual(
            strings_locale[
                "browser/chrome/browser/baseMenuOverlay.dtd:helpMenuWin.accesskey"
            ],
            "H",
        )
        self.assertEqual(
            strings_locale[
                "browser/chrome/browser/main.ftl:default-content-process-count.label"
            ],
            "{ $num } (default)",
        )
        self.assertEqual(
            strings_locale["browser/chrome/browser/main.ftl:sample"], "Just a test"
        )

        # FTL strings
        self.assertTrue("browser/chrome/browser/main.ftl:sample" in strings_locale)
        self.assertFalse(
            "browser/chrome/browser/main.ftl:default-content-process-count"
            in strings_locale
        )
        self.assertTrue(
            "browser/chrome/browser/main.ftl:default-content-process-count.label"
            in strings_locale
        )

        self.assertTrue(
            "browser/chrome/browser/main.ftl:no-value" not in strings_locale
        )
        self.assertTrue("browser/chrome/browser/main.ftl:empty-value" in strings_locale)
        self.assertEqual(
            strings_locale["browser/chrome/browser/main.ftl:empty-value"],
            "''",
        )
        self.assertEqual(
            strings_locale["browser/chrome/browser/main.ftl:empty-value.label"],
            "Test",
        )

        self.assertTrue(
            "browser/chrome/browser/main.ftl:timeDiffHoursAgo" in strings_locale
        )
        self.assertTrue(
            "*[other]"
            in strings_locale["browser/chrome/browser/main.ftl:timeDiffHoursAgo"]
        )
        self.assertTrue(
            "browser/chrome/browser/main.ftl:onboarding-fxa-text" in strings_locale
        )
        self.assertFalse(
            "browser/chrome/browser/main.ftl:default-content-process-count"
            in strings_locale
        )

    def testGetProductStringsItalian(self):
        repo_path = os.path.join(self.testfiles_path, "product", "it")
        extraction = tmx_prod.StringExtraction(self.storage_path, "it", "en-US", "test")
        extraction.setRepositoryPath(repo_path)
        extraction.extractStrings()

        strings_locale = extraction.translations
        self.assertEqual(len(strings_locale), 5)

        self.assertEqual(
            strings_locale["browser/chrome/browser/whitespaces.dtd:whitespaces"],
            "  Test 1  ",
        )
        self.assertEqual(
            strings_locale[
                "browser/chrome/browser/whitespaces.dtd:leading_whitespaces"
            ],
            "  Test 2",
        )
        self.assertEqual(
            strings_locale[
                "browser/chrome/browser/whitespaces.dtd:trailing_whitespaces"
            ],
            "Test 3  ",
        )

        self.assertEqual(
            strings_locale["browser/chrome/updater/updater.ini:Strings.TitleText"],
            "Aggiornamento %MOZ_APP_DISPLAYNAME%",
        )
        self.assertEqual(
            strings_locale["browser/chrome/updater/updater.ini:Strings.InfoText"],
            "%MOZ_APP_DISPLAYNAME% sta installando gli aggiornamenti e si avvierà fra qualche istante…",
        )

    def testGetProductStringsBulgarian(self):
        repo_path = os.path.join(self.testfiles_path, "product", "bg")
        extraction = tmx_prod.StringExtraction(self.storage_path, "bg", "en-US", "test")
        extraction.setRepositoryPath(repo_path)
        extraction.extractStrings()

        strings_locale = extraction.translations

        self.assertEqual(
            strings_locale["lightning.properties:imipBarReplyToNotExistingItem"],
            "Това съобщение съдържа отговор на събитие, което вече не е във вашия календар.                       ",
        )

    def testEscape(self):
        extraction = tmx_prod.StringExtraction(self.storage_path, "", "", "")
        extraction.translations = {
            "This is a simple test.": "This is a simple test.",
            "您的電腦中已儲存下列的 Cookie:": "您的電腦中已儲存下列的 Cookie:",
            r"Test with one \ slash character": r"Test with one \\ slash character",
            r"Test with two \\ slash characters": r"Test with two \\\\ slash characters",
            r"Retirer les caractères d’échappement \\xNN ?": r"Retirer les caractères d’échappement \\\\xNN ?",
            r"Test with unescaped single 'quotes'": r"Test with unescaped single \'quotes\'",
            r"Test with escaped single \'quotes\'": r"Test with escaped single \\\'quotes\\\'",
            r"To \&quot;Open multiple links\&quot;, please enable the \'Draw over other apps\' permission for &brandShortName;": r"To \\&quot;Open multiple links\\&quot;, please enable the \\\'Draw over other apps\\\' permission for &brandShortName;",
        }

        for string, result in extraction.translations.items():
            self.assertEqual(extraction.escape(string), result)

    def testRelativePath(self):
        extraction = tmx_prod.StringExtraction(self.storage_path, "", "", "")

        extraction.setRepositoryPath("/home/test")
        paths = {
            "/home/test/browser/branding/official/brand.dtd": "browser/branding/official/brand.dtd",
            "/home/test/browser/branding/brand.dtd": "browser/branding/brand.dtd",
            "/home/test/browser/brand.dtd": "browser/brand.dtd",
        }
        for path, result in paths.items():
            self.assertEqual(extraction.getRelativePath(path), result)

        # I should get the same results if path ends with a /
        extraction.setRepositoryPath("/home/test/")
        paths = {
            "/home/test/browser/branding/official/brand.dtd": "browser/branding/official/brand.dtd",
            "/home/test/browser/branding/brand.dtd": "browser/branding/brand.dtd",
            "/home/test/browser/brand.dtd": "browser/brand.dtd",
        }
        for path, result in paths.items():
            self.assertEqual(extraction.getRelativePath(path), result)

        # I should get the same results if path ends with a /
        extraction.setRepositoryPath("/home/test")
        extraction.setStorageAppendMode("foo/bar")
        paths = {
            "/home/test/browser/branding/official/brand.dtd": "foo/bar/browser/branding/official/brand.dtd",
            "/home/test/browser/branding/brand.dtd": "foo/bar/browser/branding/brand.dtd",
            "/home/test/browser/brand.dtd": "foo/bar/browser/brand.dtd",
        }
        for path, result in paths.items():
            self.assertEqual(extraction.getRelativePath(path), result)

    def testOutput(self):
        repo_path = os.path.join(self.testfiles_path, "tmx", "en-US")
        extraction = tmx_prod.StringExtraction(
            self.storage_path, "en-US", "en-US", "test"
        )
        extraction.setRepositoryPath(repo_path)
        extraction.extractStrings()
        extraction.storeTranslations("")

        repo_path = os.path.join(self.testfiles_path, "tmx", "it")
        extraction = tmx_prod.StringExtraction(self.storage_path, "it", "en-US", "test")
        extraction.setRepositoryPath(repo_path)
        extraction.extractStrings()
        extraction.storeTranslations("")

        # Store comparison and remove file before running the test
        output_filename = os.path.join(
            self.testfiles_path, "output", "it", "cache_it_test.php"
        )
        cmp_filename = os.path.join(self.testfiles_path, "output", "cmp_output.php")
        cmp_result_php = filecmp.cmp(output_filename, cmp_filename)

        output_filename = os.path.join(
            self.testfiles_path, "output", "it", "cache_it_test.json"
        )
        cmp_filename = os.path.join(self.testfiles_path, "output", "cmp_output.json")
        cmp_result_json = filecmp.cmp(output_filename, cmp_filename)

        # Remove files
        os.remove(
            os.path.join(self.testfiles_path, "output", "it", "cache_it_test.php")
        )
        os.remove(
            os.path.join(self.testfiles_path, "output", "it", "cache_it_test.json")
        )
        os.remove(
            os.path.join(self.testfiles_path, "output", "en-US", "cache_en-US_test.php")
        )
        os.remove(
            os.path.join(
                self.testfiles_path, "output", "en-US", "cache_en-US_test.json"
            )
        )

        self.assertTrue(cmp_result_php)
        self.assertTrue(cmp_result_json)

    def testOutputAppend(self):
        repo_path = os.path.join(self.testfiles_path, "tmx", "en-US")
        extraction = tmx_prod.StringExtraction(
            self.storage_path, "en-US", "en-US", "appendtest"
        )
        extraction.setRepositoryPath(repo_path)
        extraction.extractStrings()
        extraction.storeTranslations("")

        # Do a new extraction, but append to existing translations
        repo_path = os.path.join(self.testfiles_path, "tmx", "en-US", "mail")
        extraction = tmx_prod.StringExtraction(
            self.storage_path, "en-US", "en-US", "appendtest"
        )
        extraction.setRepositoryPath(repo_path)
        extraction.setStorageAppendMode("foo/bar/")
        extraction.extractStrings()
        extraction.storeTranslations("")

        # Store comparison and remove file before running the test
        output_filename = os.path.join(
            self.testfiles_path, "output", "en-US", "cache_en-US_appendtest.php"
        )
        cmp_filename = os.path.join(
            self.testfiles_path, "output", "cmp_output_append.php"
        )
        cmp_result_php = filecmp.cmp(output_filename, cmp_filename)

        output_filename = os.path.join(
            self.testfiles_path, "output", "en-US", "cache_en-US_appendtest.json"
        )
        cmp_filename = os.path.join(
            self.testfiles_path, "output", "cmp_output_append.json"
        )
        cmp_result_json = filecmp.cmp(output_filename, cmp_filename)

        # Remove files
        os.remove(
            os.path.join(
                self.testfiles_path, "output", "en-US", "cache_en-US_appendtest.php"
            )
        )

        os.remove(
            os.path.join(
                self.testfiles_path, "output", "en-US", "cache_en-US_appendtest.json"
            )
        )

        self.assertTrue(cmp_result_php)
        self.assertTrue(cmp_result_json)


if __name__ == "__main__":
    unittest.main()
