# -*- coding: utf-8 -*-

from script.tmx_products import create_tmx_content
import os
import unittest

import silme.core
import silme.io
import silme.format
silme.format.Manager.register('dtd', 'properties', 'ini', 'inc')


class TestCreateTMXContent(unittest.TestCase):

    def testCreateTMXProduct(self):
        testfiles_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), 'testfiles', 'tmx'))

        locale_path = os.path.join(testfiles_path, 'it')
        reference_path = os.path.join(testfiles_path, 'en-US')
        tmx_content = create_tmx_content(
            reference_path, locale_path, ['test'])

        self.assertEqual(len(tmx_content), 4)
        self.assertTrue(
            "'test/test.dtd:test1' => 'Prova con uno \\\\ slash',\n" in tmx_content)
        self.assertTrue("'test/test.dtd:test_missing' => '',\n" in tmx_content)
        self.assertFalse(
            "'test/test.dtd:test_extra' => 'Extra string: this one is not available in the reference language',\n" in tmx_content)

    def testCreateTMXGaia(self):
        testfiles_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), 'testfiles', 'gaia'))

        locale_path = os.path.join(testfiles_path, 'it')
        reference_path = os.path.join(testfiles_path, 'en-US')
        tmx_content = create_tmx_content(
            reference_path, locale_path, [''])

        self.assertEqual(len(tmx_content), 3)
        self.assertTrue(
            "'/test_root.properties:test_root' => 'Dummy file',\n" in tmx_content)
        self.assertTrue(
            "'distros/test_distros.properties:test2' => 'Dummy file',\n" in tmx_content)
        self.assertFalse(
            "'unknown/test_unknown.properties:test3' => 'Dummy file',\n" in tmx_content)

if __name__ == '__main__':
    unittest.main()
