#coding: utf-8

import sys
sys.path.append('../')
from parsed import ThreadGrabAudio

import unittest


class TestParsedThreadGrab(unittest.TestCase):
    """Test ThreadGrabAudio worker class"""

    def setUp(self):
        # stub
        queue = []
        self.t = ThreadGrabAudio(queue)
        self.filename = {'author': 'Gorillaz', 'name': 'Kids with Guns'}

    def test_normalize_name(self):
        """ Test whether normalize replaces slashes with spaces """
        name = self.t.normalize_name('\\\\test')
        name2 = self.t.normalize_name('\\test')
        name3 = self.t.normalize_name('/test')
        name4 = self.t.normalize_name('//test')

        self.assertEqual(name, ' test')
        self.assertEqual(name2, ' test')
        self.assertEqual(name3, ' test')
        self.assertEqual(name4, ' test')

    def test_normalize_separator(self):
        """ Test that normalize replaces slashes with given separator """
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

    def test_normalize_empty(self):
        name = self.t.normalize_name('')
        name2 = self.t.normalize_name('', separator='-')
        self.assertEqual(name, '')
        self.assertEqual(name2, '')

    def test_make_file(self, mf='music'):
        self.t.music_folder = mf
        filename = self.t.make_filename(self.filename)
        self.assertEqual(filename, mf+'/'+'Gorillaz - Kids with Guns.mp3')

    def test_custom_file_folder(self):
        self.test_make_file(mf='sounds')
        
    def test_default_user(self):
        pass


if __name__ == '__main__':
    unittest.main()
