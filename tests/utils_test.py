import unittest
import warnings
import sys
from src import utils

sys.path.append("../")
warnings.filterwarnings("ignore")


class Tests(unittest.TestCase):

    def test_searchSong(self):
        song_name = "Watermelon Sugar"
        actual_link = utils.searchSong(song_name)
        expected_link = "https://www.youtube.com/watch?v=E07s5ZYygMg"
        self.assertTrue(actual_link == expected_link)

    def test_random_ten(self):
        random_songs = utils.random_ten()
        self.assertTrue(len(random_songs) == 10)
