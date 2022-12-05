import unittest
import warnings
import sys

from src.get_all import *

warnings.filterwarnings("ignore")


class Tests(unittest.TestCase):

    def test_filtered_songs(self):
        filtered = filtered_songs()
        print(filtered)
        self.assertTrue(len(filtered) != 0)

    def test_get_all_songs(self):
        songs = get_all_songs()
        print(songs)
        self.assertTrue(len(songs) != 0)

    def test_recommend(self):
        ts = {"track_name": "Your Love Is My Drug", "genre": "dance pop"}
        songs = recommend(ts)
        print(songs)
        #test = {"track_name": "Living For Love", "genre": "dance pop"}
        self.assertTrue(len(songs) == 10)
