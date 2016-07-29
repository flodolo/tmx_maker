# -*- coding: utf-8 -*-

import env
import os
import unittest

from tmx_products.tmx_products import create_directories_list


class TestCreateDirectoriesList(unittest.TestCase):

    def testStandardProduct(self):
        locale_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), 'testfiles', 'product', 'zh-CN'))

        self.assertTrue(
            'browser' in create_directories_list(locale_path, '', 'aurora'))
        self.assertTrue(
            'dom' in create_directories_list(locale_path, '', 'beta'))
        self.assertFalse(
            'unknown' in create_directories_list(locale_path, '', 'test'))

if __name__ == '__main__':
    unittest.main()
