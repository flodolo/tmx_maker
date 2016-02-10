# -*- coding: utf-8 -*-

from script.tmx_products import create_directories_list
import os
import unittest


class TestCreateDirectoriesList(unittest.TestCase):

    def testStandardProduct(self):
        locale_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), 'testfiles', 'zh-CN'))

        self.assertTrue(
            'browser' in create_directories_list(locale_path, '', 'aurora'))
        self.assertTrue(
            'dom' in create_directories_list(locale_path, '', 'beta'))
        self.assertFalse(
            'unknown' in create_directories_list(locale_path, '', 'test'))

    def testGaia(self):
        testfiles_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), 'testfiles', 'gaia'))
        locale_path = os.path.join(testfiles_path, 'it')
        reference_path = os.path.join(testfiles_path, 'en-US')

        self.assertTrue(
            'apps' in create_directories_list(locale_path, reference_path, 'gaia'))
        self.assertTrue(
            'distros' in create_directories_list(locale_path, reference_path, 'gaia_2_0'))
        self.assertFalse(
            'unknown' in create_directories_list(locale_path, reference_path, 'gaia_2_5'))


if __name__ == '__main__':
    unittest.main()
