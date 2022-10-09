import unittest
import warnings
import sys
from src import utils

sys.path.append("../")
warnings.filterwarnings("ignore")


class Tests(unittest.TestCase):

    # For testing the searchSong() method. Given a song name as input, should return the youtube link.
    def test_searchSong(self):
        song_name = "Watermelon Sugar"
        actual_link = utils.searchSong(song_name)
        expected_link = "https://www.youtube.com/watch?v=E07s5ZYygMg"
        self.assertTrue(actual_link == expected_link)


# For testing the random_25() method. Checking if the list returned is of length 25.

    def test_random_25(self):
        random_songs = utils.random_25()
        self.assertTrue(len(random_songs) == 25)
