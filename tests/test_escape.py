# -*- coding: utf-8 -*-

from script.tmx_products import escape
import unittest


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
            'Retirer les caractères d’échappement \\xNN ?': 'Retirer les caractères d’échappement \\\\xNN ?',
            'Test with one \ slash': 'Test with one \\\ slash',
            "Test with one 'quotes'": "Test with one \\'quotes\\'",
            'To \&quot;Open multiple links\&quot;, please enable the \'Draw over other apps\' permission for &brandShortName;': 'To \\\\&quot;Open multiple links\\\\&quot;, please enable the \\\'Draw over other apps\\\' permission for &brandShortName;'
        }

        for string, result in strings.iteritems():
            self.assertEqual(escape(string), result)


if __name__ == '__main__':
    unittest.main()
