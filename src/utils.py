"""
This file is responsible for all the helper functions that are used
"""
from youtubesearchpython import VideosSearch
from src.get_all import filtered_songs
"""
This function seaches the song on youtube and returns the URL
"""


def searchSong(name_song):
    videosSearch = VideosSearch(name_song, limit=1)
    result = videosSearch.result()
    link = result['result'][0]['link']
    return link


all_songs = filtered_songs()[["title", "artist", "top genre"]]
"""
This function returns random 10 songs for generating the poll for the user
"""


def random_ten():
    ten_random_songs = (all_songs.sample(
        frac=1).groupby('top genre').head(1)).sample(10)
    return ten_random_songs
