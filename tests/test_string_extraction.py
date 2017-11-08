# -*- coding: utf-8 -*-

import env
import filecmp
import json
import os
import unittest

import tmx_products.tmx_products


class TestStringExtraction(unittest.TestCase):

    def setUp(self):
        self.testfiles_path = os.path.join(
            os.path.dirname(__file__), 'testfiles')
        self.storage_path = os.path.join(self.testfiles_path, 'output')

    def testGetProductStrings(self):
        repo_path = os.path.join(self.testfiles_path, 'product', 'zh-CN')
        extraction = tmx_products.tmx_products.StringExtraction(
            self.storage_path, 'zh-CN', 'en-US', 'test')
        extraction.setRepositoryPath(repo_path)
        extraction.extractStrings()

        strings_locale = extraction.translations
        self.assertEqual(len(strings_locale), 20)
        self.assertTrue(
            'browser/branding/official/brand.dtd:brandFullName' in strings_locale)
        self.assertTrue(
            'browser/branding/official/brand.properties:brandShortName' in strings_locale)
        self.assertTrue(
            'browser/defines.inc:MOZ_LANGPACK_CREATOR' in strings_locale)
        self.assertTrue(
            'dom/chrome/appstrings.properties:zeroTest' in strings_locale)
        self.assertEqual(
            strings_locale['dom/chrome/appstrings.properties:zeroTest'], '0')
        self.assertEqual(
            strings_locale['browser/chrome/browser/taskbar.properties:taskbar.tasks.newWindow.label'].encode('utf-8'), '打开新窗口')
        self.assertEqual(
            strings_locale['browser/chrome/browser/baseMenuOverlay.dtd:helpMenuWin.accesskey'].encode('utf-8'), 'H')

    def testEscape(self):
        extraction = tmx_products.tmx_products.StringExtraction(
            self.storage_path, '', '', '')
        extraction.translations = {
            'This is a simple test.': 'This is a simple test.',
            '您的電腦中已儲存下列的 Cookie:': '您的電腦中已儲存下列的 Cookie:',
            r'Test with one \ slash character': r'Test with one \\ slash character',
            r'Test with two \\ slash characters': r'Test with two \\\\ slash characters',
            r'Retirer les caractères d’échappement \\xNN ?': r'Retirer les caractères d’échappement \\\\xNN ?',
            r"Test with unescaped single 'quotes'": r"Test with unescaped single \'quotes\'",
            r"Test with escaped single \'quotes\'": r"Test with escaped single \\\'quotes\\\'",
            r"To \&quot;Open multiple links\&quot;, please enable the \'Draw over other apps\' permission for &brandShortName;": r"To \\&quot;Open multiple links\\&quot;, please enable the \\\'Draw over other apps\\\' permission for &brandShortName;"
        }

        for string, result in extraction.translations.iteritems():
            self.assertEqual(extraction.escape(string), result)

    def testRelativePath(self):
        extraction = tmx_products.tmx_products.StringExtraction(
            self.storage_path, '', '', '')

        extraction.setRepositoryPath('/home/test')
        paths = {
            '/home/test/browser/branding/official/brand.dtd': 'browser/branding/official/brand.dtd',
            '/home/test/browser/branding/brand.dtd': 'browser/branding/brand.dtd',
            '/home/test/browser/brand.dtd': 'browser/brand.dtd',
            '/home/test/browser/locales/en-US/en-US/chrome/browser/browser.dtd': 'browser/chrome/browser/browser.dtd',
            '/home/test/toolkit/locales/en-US/en-US/defines.inc': 'toolkit/defines.inc',
        }
        for path, result in paths.iteritems():
            self.assertEqual(extraction.getRelativePath(path), result)

        # I should get the same results if path ends with a /
        extraction.setRepositoryPath('/home/test/')
        paths = {
            '/home/test/browser/branding/official/brand.dtd': 'browser/branding/official/brand.dtd',
            '/home/test/browser/branding/brand.dtd': 'browser/branding/brand.dtd',
            '/home/test/browser/brand.dtd': 'browser/brand.dtd',
            '/home/test/browser/locales/en-US/en-US/chrome/browser/browser.dtd': 'browser/chrome/browser/browser.dtd',
            '/home/test/toolkit/locales/en-US/en-US/defines.inc': 'toolkit/defines.inc',
        }
        for path, result in paths.iteritems():
            self.assertEqual(extraction.getRelativePath(path), result)

        # I should get the same results if path ends with a /
        extraction.setRepositoryPath('/home/test')
        extraction.setStorageMode('append', 'foo/bar')
        paths = {
            '/home/test/browser/branding/official/brand.dtd': 'foo/bar/browser/branding/official/brand.dtd',
            '/home/test/browser/branding/brand.dtd': 'foo/bar/browser/branding/brand.dtd',
            '/home/test/browser/brand.dtd': 'foo/bar/browser/brand.dtd',
            '/home/test/browser/locales/en-US/en-US/chrome/browser/browser.dtd': 'foo/bar/browser/chrome/browser/browser.dtd',
            '/home/test/toolkit/locales/en-US/en-US/defines.inc': 'foo/bar/toolkit/defines.inc',
        }
        for path, result in paths.iteritems():
            self.assertEqual(extraction.getRelativePath(path), result)

    def testOutput(self):
        repo_path = os.path.join(self.testfiles_path, 'tmx', 'en-US')
        extraction = tmx_products.tmx_products.StringExtraction(
            self.storage_path, 'en-US', 'en-US', 'test')
        extraction.setRepositoryPath(repo_path)
        extraction.extractStrings()
        extraction.storeTranslations('')

        repo_path = os.path.join(self.testfiles_path, 'tmx', 'it')
        extraction = tmx_products.tmx_products.StringExtraction(
            self.storage_path, 'it', 'en-US', 'test')
        extraction.setRepositoryPath(repo_path)
        extraction.extractStrings()
        extraction.storeTranslations('')

        # Store comparison and remove file before running the test
        output_filename = os.path.join(
            self.testfiles_path, 'output', 'it', 'cache_it_test.php')
        cmp_filename = os.path.join(
            self.testfiles_path, 'output', 'cmp_output.php')
        cmp_result_php = filecmp.cmp(output_filename, cmp_filename)

        output_filename = os.path.join(
            self.testfiles_path, 'output', 'it', 'cache_it_test.json')
        cmp_filename = os.path.join(
            self.testfiles_path, 'output', 'cmp_output.json')
        cmp_result_json = filecmp.cmp(output_filename, cmp_filename)

        # Remove files
        os.remove(os.path.join(self.testfiles_path,
                               'output', 'it', 'cache_it_test.php'))
        os.remove(os.path.join(self.testfiles_path,
                               'output', 'it', 'cache_it_test.json'))
        os.remove(os.path.join(self.testfiles_path,
                               'output', 'en-US', 'cache_en-US_test.php'))
        os.remove(os.path.join(self.testfiles_path, 'output',
                               'en-US', 'cache_en-US_test.json'))

        self.assertTrue(cmp_result_php)
        self.assertTrue(cmp_result_json)

    def testOutputAppend(self):
        repo_path = os.path.join(self.testfiles_path, 'tmx', 'en-US')
        extraction = tmx_products.tmx_products.StringExtraction(
            self.storage_path, 'en-US', 'en-US', 'appendtest')
        extraction.setRepositoryPath(repo_path)
        extraction.extractStrings()
        extraction.storeTranslations('')

        # Do a new extraction, but append to existing translations
        repo_path = os.path.join(self.testfiles_path, 'tmx', 'en-US', 'mail')
        extraction = tmx_products.tmx_products.StringExtraction(
            self.storage_path, 'en-US', 'en-US', 'appendtest')
        extraction.setRepositoryPath(repo_path)
        extraction.setStorageMode('append', 'foo/bar/')
        extraction.extractStrings()
        extraction.storeTranslations('')

        # Store comparison and remove file before running the test
        output_filename = os.path.join(
            self.testfiles_path, 'output', 'en-US', 'cache_en-US_appendtest.php')
        cmp_filename = os.path.join(
            self.testfiles_path, 'output', 'cmp_output_append.php')
        cmp_result_php = filecmp.cmp(output_filename, cmp_filename)

        output_filename = os.path.join(
            self.testfiles_path, 'output', 'en-US', 'cache_en-US_appendtest.json')
        cmp_filename = os.path.join(
            self.testfiles_path, 'output', 'cmp_output_append.json')
        cmp_result_json = filecmp.cmp(output_filename, cmp_filename)

        # Remove files
        os.remove(os.path.join(self.testfiles_path,
                               'output', 'en-US', 'cache_en-US_appendtest.php'))
        os.remove(os.path.join(self.testfiles_path, 'output',
                               'en-US', 'cache_en-US_appendtest.json'))

        self.assertTrue(cmp_result_php)
        self.assertTrue(cmp_result_json)

    def testBrokenEnconding(self):
        repo_path = os.path.join(self.testfiles_path, 'tmx', 'oc')
        extraction = tmx_products.tmx_products.StringExtraction(
            self.storage_path, 'oc', 'en-US', 'test')
        extraction.setRepositoryPath(repo_path)
        extraction.extractStrings()

        self.assertEqual(extraction.translations[
                         'test/test.dtd:test1'], 'Test with one \ slash')
        self.assertFalse(
            'test/test.dtd:test_missing' in extraction.translations)
        self.assertFalse('test/test.dtd:test_empty' in extraction.translations)


if __name__ == '__main__':
    unittest.main()
