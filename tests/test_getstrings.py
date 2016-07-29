# -*- coding: utf-8 -*-

import env
import os
import unittest

from tmx_products.tmx_products import get_strings

import silme.core
import silme.io
import silme.format
silme.format.Manager.register('dtd', 'properties', 'ini', 'inc')


class TestGetStrings(unittest.TestCase):

    def testGetProductStrings(self):
        testfiles_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), 'testfiles'))

        rcsClient = silme.io.Manager.get('file')
        locale_path = os.path.join(
            testfiles_path, 'product', 'zh-CN', 'browser')
        l10nPackage_locale = rcsClient.get_package(
            locale_path, object_type='entitylist')

        strings_locale = {}
        get_strings(l10nPackage_locale, 'browser', strings_locale)

        self.assertEqual(len(strings_locale), 14)
        self.assertTrue(
            'browser/branding/official/brand.dtd:brandFullName' in strings_locale)
        self.assertTrue(
            'browser/branding/official/brand.properties:brandShortName' in strings_locale)
        self.assertTrue(
            'browser/defines.inc:MOZ_LANGPACK_CREATOR' in strings_locale)
        self.assertEqual(
            strings_locale['browser/chrome/browser/taskbar.properties:taskbar.tasks.newWindow.label'].encode('utf-8'), '打开新窗口')
        self.assertEqual(
            strings_locale['browser/chrome/browser/baseMenuOverlay.dtd:helpMenuWin.accesskey'].encode('utf-8'), 'H')

if __name__ == '__main__':
    unittest.main()
