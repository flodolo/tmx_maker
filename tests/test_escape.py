# -*- coding: utf-8 -*-

import env
import unittest

from tmx_products.tmx_products import escape

class TestEscape(unittest.TestCase):

    def testCleanStrings(self):
        strings = {
            'This is a simple test.': 'This is a simple test.',
            '您的電腦中已儲存下列的 Cookie:': '您的電腦中已儲存下列的 Cookie:'
        }

        for string, result in strings.iteritems():
            self.assertEqual(escape(string), result)

    def testEscapedStrings(self):
        strings = {
            r'Test with one \ slash character': r'Test with one \\ slash character',
            r'Test with two \\ slash characters': r'Test with two \\\\ slash characters',
            r'Retirer les caractères d’échappement \\xNN ?': r'Retirer les caractères d’échappement \\\\xNN ?',
            r"Test with unescaped single 'quotes'": r"Test with unescaped single \'quotes\'",
            r"Test with escaped single \'quotes\'": r"Test with escaped single \\\'quotes\\\'",
            r"To \&quot;Open multiple links\&quot;, please enable the \'Draw over other apps\' permission for &brandShortName;": r"To \\&quot;Open multiple links\\&quot;, please enable the \\\'Draw over other apps\\\' permission for &brandShortName;"
        }

        for string, result in strings.iteritems():
            self.assertEqual(escape(string), result)


if __name__ == '__main__':
    unittest.main()
