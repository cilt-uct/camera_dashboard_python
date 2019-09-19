import unittest
from ..utils import contains_unusual_characters, get_camera_url
from .test_helper import *


class Test(unittest.TestCase):

    def test_contains_unusual_characters_passing(self):
        self.assertTrue(contains_unusual_characters(venues[0]))

    def test_contains_unusual_characters_failing(self):
        self.assertFalse(contains_unusual_characters(venues[1]))

    def test_contains_unusual_characters_failing1(self):
        self.assertFalse(contains_unusual_characters(venues[2]))

    def test_contains_unusual_characters_failing2(self):
        self.assertFalse(contains_unusual_characters(venues[3]))

    def test_get_camera_url_rtsp(self):
        self.assertEqual("rtsp://test.uct/test", get_camera_url(items_rtsp))

    def test_get_camera_url_rtspt(self):
        self.assertEqual("rtsp://test.uct/test", get_camera_url(items_rtspt))

    def test_get_camera_url_no_url(self):
        self.assertEqual("", get_camera_url(items_no_url))


if __name__ == '__main__':
    unittest.main()
