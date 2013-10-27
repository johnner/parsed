#coding: utf-8

import sys
sys.path.append('../')
from parsed import ThreadGrabAudio

import unittest

class TestParsedThreadGrab(unittest.TestCase):
    """Test ThreadGrabAudio worker class"""

    def setUp(self):
        queue = [] #mock
#        self.uid = 123
#        self.login = 'test'
#        self.passwd = 'test'
        self.t = ThreadGrabAudio(queue)


    def test_normalize_name(self):
        """Test whether normalize replaces slashes with spaces
        """
        name = self.t.normalize_name('\\\\test')
        name2 = self.t.normalize_name('\\test')
        name3 = self.t.normalize_name('/test')
        name4 = self.t.normalize_name('//test')

        self.assertEqual(name, ' test')
        self.assertEqual(name2, ' test')
        self.assertEqual(name3, ' test')
        self.assertEqual(name4, ' test')


    def test_normalize_separator(self):
        """Test that normalize replaces slashes with given separator"""
        sep = '-'
        text = 'test'
        expected = sep + text
        name = self.t.normalize_name('\\\\' + text, separator=sep)
        name2 = self.t.normalize_name('\\' + text, separator=sep)
        name3 = self.t.normalize_name('/' + text, separator=sep)
        name4 = self.t.normalize_name('//' + text, separator=sep)

        self.assertEqual(name, expected)
        self.assertEqual(name2, expected)
        self.assertEqual(name3, expected)
        self.assertEqual(name4, expected)


if __name__ == '__main__':
    unittest.main()
