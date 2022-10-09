import pytest
import unittest
from src.songs_cog import *
import warnings
import sys

sys.path.append("../")

warnings.filterwarnings("ignore")

@pytest.mark.asyncio
class Test_Songs_Cog(unittest.TestCase):
    async def test_resume(self):
        result = await Songs.resume()
        assert result == "The bot was not playing anything before this. Use play command"
