#coding: utf-8

import sys
sys.path.append('../')
from parsed import ThreadGrabAudio

import unittest

class TestParsed(unittest.TestCase):

    def setUp(self):
        self.uid = 123
        self.login = 'test'
        self.passwd = 'test'

    def test_normalize_name(self):
        queue_mock = {}
        t = ThreadGrabAudio(queue_mock)
        name = t.normalize_name('\\test')
        self.assertEqual(name, 'test', 'slashes are not cutted')

if __name__ == '__main__':
    unittest.main()
