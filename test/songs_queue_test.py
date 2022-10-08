import unittest
import warnings
import sys

sys.path.append("../")
from src.songs_queue import Songs_Queue

warnings.filterwarnings("ignore")

class Tests(unittest.TestCase):
	def test_next_song(self):
		song_names = ["a","b","c","d"]
		sq = Songs_Queue(song_names)
		ts = [song_names]
		function = sq.next_song()
		self.assertTrue("a" == function)
