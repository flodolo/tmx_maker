# -*- coding: utf-8 -*-

import env
import filecmp
import os
import unittest

from tmx_products.tmx_products import create_tmx_content
from tmx_products.tmx_products import write_php_file

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

        self.assertEqual(len(tmx_content), 5)
        self.assertTrue(
            "'test/test.dtd:test1' => 'Prova con uno \\\\ slash'" in tmx_content)
        self.assertFalse(
            "'test/test.dtd:test_extra' => 'Extra string: this one is not available in the reference language'" in tmx_content)
        self.assertFalse(
            "'test/test.dtd:test_missing' => ''" in tmx_content)
        self.assertTrue(
            "'test/test.dtd:test_empty' => ''" in tmx_content)

    def testCreateTMXEncodingError(self):
        testfiles_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), 'testfiles', 'tmx'))

        locale_path = os.path.join(testfiles_path, 'oc')
        reference_path = os.path.join(testfiles_path, 'en-US')
        tmx_content = create_tmx_content(
            reference_path, locale_path, ['mail', 'test'])

        self.assertEqual(len(tmx_content), 3)
        self.assertTrue(
            "'test/test.dtd:test1' => 'Test with one \\\\ slash'" in tmx_content)
        self.assertFalse(
            "'test/test.dtd:test_missing' => 'This one won\\'t be translated in the locale'" in tmx_content)

    def testPHPOutput(self):
        testfiles_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), 'testfiles'))

        locale_path = os.path.join(testfiles_path, 'tmx', 'it')
        reference_path = os.path.join(testfiles_path, 'tmx', 'en-US')
        tmx_content = create_tmx_content(
            reference_path, locale_path, ['test'])

        output_filename = os.path.join(testfiles_path, 'output', 'tmp.php')
        write_php_file(output_filename, tmx_content)

        # Store comparison and remove file before running the test
        cmp_filename = os.path.join(testfiles_path, 'output', 'cmp_output.php')
        cmp_result = filecmp.cmp(output_filename, cmp_filename)
        os.remove(output_filename)

        self.assertTrue(cmp_result)


if __name__ == '__main__':
    unittest.main()
